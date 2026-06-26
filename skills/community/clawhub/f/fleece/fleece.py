"""
Fleece — AI-powered credit card advisor chatbot.
# Author: Yuan Chen
# Date: March 16, 2025
"""
import os

import streamlit as st
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from prompts.agent_system_prompt import build_system_prompt
import db

# ---------------------------------------------------------------------------
# Page config + CSS
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Fleece — Find the best card for deal saviors",
    page_icon="🟡",
    layout="wide",
)


def load_css():
    # Google Fonts
    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700'
        '&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


try:
    load_css()
except Exception as e:
    st.warning(f"Could not load custom styling: {e}")

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_text():
    """Return the current user input from the text box."""
    return st.text_input(
        "You: ",
        st.session_state["input"],
        key="input",
        placeholder="Your AI assistant here! Ask me anything ...",
        label_visibility="hidden",
    )


def new_chat():
    """Archive the current conversation and start fresh."""
    save = []
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.entity_store = {}
    st.session_state.entity_memory.buffer.clear()


# ---------------------------------------------------------------------------
# Sidebar — API key (env first, text input as fallback)
# ---------------------------------------------------------------------------

_env_key = os.getenv("OPENAI_API_KEY", "")
if _env_key:
    API_O = _env_key
    st.sidebar.success("OpenAI key loaded from environment")
else:
    API_O = st.sidebar.text_input("OpenAI API Key", type="password",
                                  placeholder="sk-...",
                                  help="Or set OPENAI_API_KEY in your environment")

# ---------------------------------------------------------------------------
# Sidebar — visible settings
# ---------------------------------------------------------------------------

st.sidebar.markdown("## Model")
MODEL = st.sidebar.selectbox(
    label="Model",
    options=["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
    index=0,
    label_visibility="collapsed",
)
K = st.sidebar.slider("Memory depth (K)", min_value=2, max_value=20, value=5,
                      help="Number of recent exchanges kept in entity memory")

# ---------------------------------------------------------------------------
# Sidebar — debug expander
# ---------------------------------------------------------------------------

with st.sidebar.expander("Debug", expanded=False):
    show_tool_calls = st.checkbox("Show tool calls", value=False)
    if st.checkbox("Memory store"):
        if "entity_memory" in st.session_state and hasattr(st.session_state.entity_memory, "store"):
            st.write(st.session_state.entity_memory.store)
        else:
            st.write("Not initialized.")
    if st.checkbox("Memory buffer"):
        if "entity_memory" in st.session_state and hasattr(st.session_state.entity_memory, "buffer"):
            st.write(st.session_state.entity_memory.buffer)
        else:
            st.write("Not initialized.")

# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------

st.markdown(
    '<h1 style="color:#111111;font-family:Oswald,sans-serif;font-weight:700;'
    'text-transform:uppercase;letter-spacing:1px;border-bottom:3px solid #FFD100;'
    'padding-bottom:0.4rem;margin-bottom:0.25rem;">Fleece</h1>'
    '<p style="color:#555555;font-family:\'Source Sans 3\',sans-serif;font-size:1rem;'
    'margin-top:0;margin-bottom:1.25rem;">Find the best card for deal saviors</p>',
    unsafe_allow_html=True,
)
st.info("💡 Navigate to the Credit Cards page to explore available cards or My Credit Cards to manage your existing cards!")

# ---------------------------------------------------------------------------
# Agent setup (runs on every Streamlit rerender — cheap, stateless object)
# ---------------------------------------------------------------------------

if API_O:
    llm = ChatOpenAI(temperature=0, api_key=API_O, model_name=MODEL, verbose=False)

    if "entity_memory" not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(
            llm=llm,
            k=K,
            chat_history_key="chat_history",
            return_messages=True,
        )

    brave_key = os.getenv("BRAVE_API_KEY", "")

    try:
        from tools import build_tools
        tools = build_tools(brave_key) if brave_key else []
    except Exception:
        tools = []

    # Pre-load profile and wallet from fleece.db into the system prompt
    try:
        profile_ctx = db.profile_as_context()
        card_names  = db.get_card_names()
        wallet_ctx  = ", ".join(card_names) if card_names else ""
    except Exception:
        profile_ctx = ""
        wallet_ctx  = ""

    system_prompt = build_system_prompt(profile_ctx, wallet_ctx)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=st.session_state.entity_memory,
        handle_parsing_errors=True,
        max_iterations=5,
        max_execution_time=150.0,
        verbose=False,
        return_intermediate_steps=show_tool_calls,
    )

    # Sidebar — profile & wallet status
    st.sidebar.markdown("## Research")
    if brave_key:
        st.sidebar.success(f"Live research enabled ({len(tools)} tools)")
    else:
        st.sidebar.info("Set BRAVE_API_KEY to enable live card data.")

    if profile_ctx:
        st.sidebar.markdown("## Profile")
        st.sidebar.caption(profile_ctx)
    if wallet_ctx:
        st.sidebar.markdown("## Wallet")
        st.sidebar.caption(wallet_ctx)

else:
    if not _env_key:
        st.sidebar.warning("Enter your OpenAI API key above to get started. It is not stored.")

# ---------------------------------------------------------------------------
# Sidebar — navigation and actions
# ---------------------------------------------------------------------------

st.sidebar.markdown("## Navigation")
st.sidebar.info("Use the sidebar menu ↑ to navigate between pages")

st.sidebar.markdown("## Actions")
st.sidebar.button("New Chat", on_click=new_chat, type="primary")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Credit Cards", type="secondary"):
        st.info("Please use the sidebar navigation menu to view the Credit Cards page")
with col2:
    if st.button("My Cards", type="secondary"):
        st.info("Please use the sidebar navigation menu to view the My Credit Cards page")

# ---------------------------------------------------------------------------
# Conversation — input → agent → display
# ---------------------------------------------------------------------------

user_input = get_text()

if user_input and API_O:
    with st.status("Thinking...", expanded=False) as status:
        try:
            result = agent_executor.invoke({"input": user_input})
            output = result["output"]

            if show_tool_calls and result.get("intermediate_steps"):
                st.write("**Tools used:**")
                for action, _ in result["intermediate_steps"]:
                    st.write(f"- `{action.tool}` ← {action.tool_input}")

            status.update(label="Done", state="complete", expanded=False)
        except Exception as e:
            error_type = type(e).__name__
            if "RateLimit" in error_type:
                output = "I've hit the API rate limit. Please wait a moment and try again."
            elif "Timeout" in error_type or "Connection" in error_type:
                output = "Research is temporarily unavailable. I'll answer from my training data instead. Please try again shortly."
            else:
                output = "I encountered an error processing your request. Please try rephrasing your question."
            status.update(label="Error", state="error", expanded=False)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# ---------------------------------------------------------------------------
# Conversation history display
# ---------------------------------------------------------------------------

download_str = []
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.info(st.session_state["past"][i], icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])

    download_str = "\n".join(download_str)
    if download_str:
        st.download_button("Download", download_str)

# ---------------------------------------------------------------------------
# Stored sessions
# ---------------------------------------------------------------------------

for i, sublist in enumerate(st.session_state.stored_session):
    with st.sidebar.expander(label=f"Conversation-Session:{i}"):
        st.write(sublist)

if st.session_state.stored_session:
    if st.sidebar.checkbox("Clear-all"):
        del st.session_state.stored_session
