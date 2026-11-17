"""错误码与可预期错误。所有技能用同一套错误码，便于 Agent 按代码判断下一步。"""

E_SVD_NOT_FOUND = "E_SVD_NOT_FOUND"
E_SVD_PARSE = "E_SVD_PARSE"
E_PERIPH_NOT_FOUND = "E_PERIPH_NOT_FOUND"
E_REG_NOT_FOUND = "E_REG_NOT_FOUND"
E_FIELD_NOT_FOUND = "E_FIELD_NOT_FOUND"
E_INPUT_INVALID = "E_INPUT_INVALID"
E_NOT_SUPPORTED = "E_NOT_SUPPORTED"
E_INTERNAL = "E_INTERNAL"


class EtkError(Exception):
    """可预期的错误：携带错误码、说明、修复提示和可选细节（如候选名、已尝试的位置）。"""

    def __init__(self, code, message, hint=None, details=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.hint = hint
        self.details = details or {}

    def to_dict(self):
        out = {"code": self.code, "message": self.message, "hint": self.hint}
        if self.details:
            out["details"] = self.details
        return out
