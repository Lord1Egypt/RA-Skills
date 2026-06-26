// Structured JSON output protocol — every command emits one of these to
// stdout. Mirrors the convention used by predict-agent / community-agent
// so an LLM can chain commands by reading `_internal.next_command`.

use serde::Serialize;
use serde_json::{json, Value};

#[derive(Serialize, Default, Debug)]
pub struct Internal {
    pub next_action: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub next_command: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub progress: Option<String>,
}

#[derive(Serialize, Debug)]
pub struct Output {
    pub status: String,
    pub message: String,
    #[serde(skip_serializing_if = "Value::is_null")]
    pub data: Value,
    #[serde(rename = "_internal")]
    pub internal: Internal,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error_code: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error_kind: Option<String>,
    #[serde(skip_serializing_if = "Value::is_null")]
    pub debug: Value,
}

impl Output {
    pub fn success(message: impl Into<String>, data: Value, internal: Internal) -> Self {
        Self {
            status: "ok".into(),
            message: message.into(),
            data,
            internal,
            error_code: None,
            error_kind: None,
            debug: Value::Null,
        }
    }

    pub fn error(
        message: impl Into<String>,
        code: impl Into<String>,
        kind: impl Into<String>,
        retryable: bool,
        suggestion: impl Into<String>,
        internal: Internal,
    ) -> Self {
        Self {
            status: "error".into(),
            message: message.into(),
            data: json!({ "retryable": retryable, "suggestion": suggestion.into() }),
            internal,
            error_code: Some(code.into()),
            error_kind: Some(kind.into()),
            debug: Value::Null,
        }
    }

    pub fn error_with_debug(
        message: impl Into<String>,
        code: impl Into<String>,
        kind: impl Into<String>,
        retryable: bool,
        suggestion: impl Into<String>,
        debug: Value,
        internal: Internal,
    ) -> Self {
        let mut o = Self::error(message, code, kind, retryable, suggestion, internal);
        o.debug = debug;
        o
    }

    pub fn print(&self) {
        println!("{}", serde_json::to_string_pretty(self).unwrap());
    }
}
