// Session Store – persisted session storage (stub)
// Mirrored from Python src/session_store.py
export function loadSession(_sessionId) {
    return {
        session_id: _sessionId,
        messages: [],
        input_tokens: 0,
        output_tokens: 0,
    };
}
export function saveSession(_session) {
    return `<session_store_path>/${_session.session_id}.json`;
}
