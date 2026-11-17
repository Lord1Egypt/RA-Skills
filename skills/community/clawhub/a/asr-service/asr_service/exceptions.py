"""ASR-Service 异常"""


class ASRServiceError(Exception):
    """ASR 服务不可用"""
    pass


class ASRTranscriptionError(Exception):
    """转写失败"""
    pass
