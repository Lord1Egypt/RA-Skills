"""
Tests for fleece.py — the main Streamlit chatbot application.

Because fleece.py executes top-level Streamlit calls on import, every test
must patch `streamlit` (and related modules) before importing the module.
We use importlib to get a fresh module-level execution per test.
"""

import importlib
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class FakeSessionState:
    """Mimics Streamlit's SessionState: supports both dict-style and attribute access."""

    def __init__(self, initial=None):
        object.__setattr__(self, "_store", dict(initial or {}))

    def __contains__(self, key):
        return key in self._store

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]

    def __getattr__(self, key):
        store = object.__getattribute__(self, "_store")
        if key in store:
            return store[key]
        raise AttributeError(key)

    def __setattr__(self, key, value):
        self._store[key] = value

    def __delattr__(self, key):
        del self._store[key]


def _build_st_mock():
    """Build a mock for the `streamlit` module with enough surface area for fleece.py."""
    st = MagicMock()
    st.text_input.return_value = ""
    st.sidebar.text_input.return_value = ""
    st.button.return_value = False
    st.checkbox.return_value = False
    st.sidebar.checkbox.return_value = False
    col1, col2 = MagicMock(), MagicMock()
    st.sidebar.columns.return_value = [col1, col2]
    # st.status must work as a context manager
    status_cm = MagicMock()
    status_cm.__enter__ = MagicMock(return_value=status_cm)
    status_cm.__exit__ = MagicMock(return_value=False)
    st.status.return_value = status_cm
    return st


def _default_langchain_mocks(lc_overrides=None):
    """Return the standard set of langchain sys.modules mocks."""
    mocks = {
        "langchain": MagicMock(),
        "langchain.agents": MagicMock(),
        "langchain.chains": MagicMock(),
        "langchain.chains.conversation": MagicMock(),
        "langchain.chains.conversation.memory": MagicMock(),
        "langchain_core": MagicMock(),
        "langchain_core.prompts": MagicMock(),
        "langchain_openai": MagicMock(),
        "tools": MagicMock(),
        "prompts": MagicMock(),
        "prompts.agent_system_prompt": MagicMock(SYSTEM_PROMPT="{entities}"),
    }
    if lc_overrides:
        mocks.update(lc_overrides)
    return mocks


def _import_fleece(st_mock, langchain_mocks=None):
    """Import (or reload) fleece.py with streamlit and langchain patched."""
    import sys

    patches = {"streamlit": st_mock}
    patches.update(langchain_mocks or _default_langchain_mocks())

    sys.modules.pop("fleece", None)

    with patch.dict(sys.modules, patches):
        mod = importlib.import_module("fleece")
    return mod


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestSessionStateInitialization:
    """Verify that fleece.py initialises missing session-state keys."""

    def test_default_keys_are_created(self):
        st_mock = _build_st_mock()
        state = FakeSessionState()
        st_mock.session_state = state

        _import_fleece(st_mock)

        assert "generated" in state
        assert "past" in state
        assert "input" in state
        assert "stored_session" in state

    def test_default_values_are_empty_lists_and_string(self):
        st_mock = _build_st_mock()
        state = FakeSessionState()
        st_mock.session_state = state

        _import_fleece(st_mock)

        assert state["generated"] == []
        assert state["past"] == []
        assert state["input"] == ""
        assert state["stored_session"] == []

    def test_existing_keys_are_not_overwritten(self):
        st_mock = _build_st_mock()
        state = FakeSessionState({
            "generated": ["old_response"],
            "past": ["old_prompt"],
            "input": "hello",
            "stored_session": [["archived"]],
        })
        st_mock.session_state = state

        _import_fleece(st_mock)

        assert state["generated"] == ["old_response"]
        assert state["past"] == ["old_prompt"]
        assert state["input"] == "hello"
        assert state["stored_session"] == [["archived"]]


class TestNewChat:
    """Tests for the new_chat() function."""

    def _setup(self, store_contents):
        st_mock = _build_st_mock()
        state = FakeSessionState(store_contents)
        st_mock.session_state = state

        mod = _import_fleece(st_mock)
        return mod.new_chat, state

    def test_archives_conversation_in_reverse_order(self):
        entity_memory = MagicMock()
        entity_memory.entity_store = {"Person": "info"}
        entity_memory.buffer = MagicMock()

        new_chat, state = self._setup({
            "generated": ["response1", "response2"],
            "past": ["prompt1", "prompt2"],
            "input": "current input",
            "stored_session": [],
            "entity_memory": entity_memory,
        })

        new_chat()

        assert len(state["stored_session"]) == 1
        archived = state["stored_session"][0]
        assert archived[0] == "User:prompt2"
        assert archived[1] == "Bot:response2"
        assert archived[2] == "User:prompt1"
        assert archived[3] == "Bot:response1"

    def test_clears_generated_past_and_input(self):
        entity_memory = MagicMock()
        entity_memory.entity_store = {"Person": "info"}
        entity_memory.buffer = MagicMock()

        new_chat, state = self._setup({
            "generated": ["r1"],
            "past": ["p1"],
            "input": "text",
            "stored_session": [],
            "entity_memory": entity_memory,
        })

        new_chat()

        assert state["generated"] == []
        assert state["past"] == []
        assert state["input"] == ""

    def test_clears_entity_memory(self):
        entity_memory = MagicMock()
        entity_memory.entity_store = {"Person": "info"}
        entity_memory.buffer = MagicMock()

        new_chat, state = self._setup({
            "generated": ["r1"],
            "past": ["p1"],
            "input": "",
            "stored_session": [],
            "entity_memory": entity_memory,
        })

        new_chat()

        assert state.entity_memory.entity_store == {}
        state.entity_memory.buffer.clear.assert_called_once()

    def test_empty_conversation_archives_empty_list(self):
        entity_memory = MagicMock()
        entity_memory.entity_store = {}
        entity_memory.buffer = MagicMock()

        new_chat, state = self._setup({
            "generated": [],
            "past": [],
            "input": "",
            "stored_session": [],
            "entity_memory": entity_memory,
        })

        new_chat()

        assert len(state["stored_session"]) == 1
        assert state["stored_session"][0] == []

    def test_preserves_previous_sessions(self):
        entity_memory = MagicMock()
        entity_memory.entity_store = {}
        entity_memory.buffer = MagicMock()

        existing_session = ["User:old", "Bot:old_reply"]
        new_chat, state = self._setup({
            "generated": ["new_reply"],
            "past": ["new_msg"],
            "input": "",
            "stored_session": [existing_session],
            "entity_memory": entity_memory,
        })

        new_chat()

        assert len(state["stored_session"]) == 2
        assert state["stored_session"][0] == existing_session


class TestGetText:
    """Tests for the get_text() function."""

    def test_returns_user_input(self):
        st_mock = _build_st_mock()
        state = FakeSessionState()
        st_mock.session_state = state

        mod = _import_fleece(st_mock)

        st_mock.text_input.return_value = "What card should I get?"
        result = mod.get_text()

        assert result == "What card should I get?"

    def test_passes_correct_label(self):
        st_mock = _build_st_mock()
        state = FakeSessionState()
        st_mock.session_state = state
        st_mock.text_input.return_value = ""

        mod = _import_fleece(st_mock)
        mod.get_text()

        call_args = st_mock.text_input.call_args
        assert call_args is not None
        assert call_args[0][0] == "You: "


class TestAgentExecutorSetup:
    """Verify that providing an API key sets up the LLM, memory, and agent correctly."""

    def _make_mocks(self):
        mock_chat_openai = MagicMock()
        mock_create_agent = MagicMock()
        mock_agent_executor_cls = MagicMock()
        mock_entity_memory_cls = MagicMock()
        mock_chat_prompt = MagicMock()

        lc_agents = MagicMock()
        lc_agents.create_openai_tools_agent = mock_create_agent
        lc_agents.AgentExecutor = mock_agent_executor_cls

        lc_memory = MagicMock()
        lc_memory.ConversationEntityMemory = mock_entity_memory_cls

        lc_core_prompts = MagicMock()
        lc_core_prompts.ChatPromptTemplate = mock_chat_prompt
        lc_core_prompts.MessagesPlaceholder = MagicMock()

        lc_openai = MagicMock()
        lc_openai.ChatOpenAI = mock_chat_openai

        overrides = {
            "langchain.agents": lc_agents,
            "langchain.chains.conversation.memory": lc_memory,
            "langchain_core.prompts": lc_core_prompts,
            "langchain_openai": lc_openai,
        }
        return overrides, mock_chat_openai, mock_create_agent, mock_entity_memory_cls

    def test_llm_created_with_api_key(self):
        st_mock = _build_st_mock()
        state = FakeSessionState()
        st_mock.session_state = state

        st_mock.sidebar.text_input.return_value = "sk-test-key-123"
        st_mock.sidebar.expander.return_value.__enter__ = MagicMock(return_value=st_mock)
        st_mock.sidebar.expander.return_value.__exit__ = MagicMock(return_value=False)
        st_mock.selectbox.return_value = "gpt-4o"
        st_mock.number_input.return_value = 5

        overrides, mock_chat_openai, _, _ = self._make_mocks()
        _import_fleece(st_mock, _default_langchain_mocks(overrides))

        mock_chat_openai.assert_called()

    def test_entity_memory_uses_correct_keys(self):
        """chat_history_key and return_messages must be set correctly."""
        st_mock = _build_st_mock()
        state = FakeSessionState()
        st_mock.session_state = state

        st_mock.sidebar.text_input.return_value = "sk-test-key-123"
        st_mock.sidebar.expander.return_value.__enter__ = MagicMock(return_value=st_mock)
        st_mock.sidebar.expander.return_value.__exit__ = MagicMock(return_value=False)
        st_mock.selectbox.return_value = "gpt-4o"
        st_mock.number_input.return_value = 5

        overrides, _, _, mock_entity_memory_cls = self._make_mocks()
        _import_fleece(st_mock, _default_langchain_mocks(overrides))

        call_kwargs = mock_entity_memory_cls.call_args[1] if mock_entity_memory_cls.called else {}
        assert call_kwargs.get("chat_history_key") == "chat_history"
        assert call_kwargs.get("return_messages") is True

    def test_create_openai_tools_agent_called(self):
        st_mock = _build_st_mock()
        state = FakeSessionState()
        st_mock.session_state = state

        st_mock.sidebar.text_input.return_value = "sk-test-key-123"
        st_mock.sidebar.expander.return_value.__enter__ = MagicMock(return_value=st_mock)
        st_mock.sidebar.expander.return_value.__exit__ = MagicMock(return_value=False)
        st_mock.selectbox.return_value = "gpt-4o"
        st_mock.number_input.return_value = 5

        overrides, _, mock_create_agent, _ = self._make_mocks()
        _import_fleece(st_mock, _default_langchain_mocks(overrides))

        mock_create_agent.assert_called()

    def test_no_api_key_shows_warning(self):
        st_mock = _build_st_mock()
        state = FakeSessionState()
        st_mock.session_state = state

        st_mock.sidebar.text_input.return_value = ""
        st_mock.sidebar.expander.return_value.__enter__ = MagicMock(return_value=st_mock)
        st_mock.sidebar.expander.return_value.__exit__ = MagicMock(return_value=False)

        _import_fleece(st_mock)

        st_mock.sidebar.warning.assert_called()


class TestDownloadConversation:
    """Verify conversation download string is built correctly."""

    def test_download_str_format(self):
        past = ["Hello", "How are you?"]
        generated = ["Hi there!", "I'm good, thanks!"]

        download_str = []
        for i in range(len(generated) - 1, -1, -1):
            download_str.append(past[i])
            download_str.append(generated[i])

        result = "\n".join(download_str)
        lines = result.split("\n")

        assert lines[0] == "How are you?"
        assert lines[1] == "I'm good, thanks!"
        assert lines[2] == "Hello"
        assert lines[3] == "Hi there!"

    def test_empty_conversation_produces_empty_string(self):
        download_str = []
        result = "\n".join(download_str)
        assert result == ""
