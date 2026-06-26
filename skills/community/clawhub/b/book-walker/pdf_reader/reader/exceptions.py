"""自定义异常 - PDF Reader"""


class PDFReaderError(Exception):
    """基础异常"""
    pass


class PDFEncrypted(PDFReaderError):
    """PDF加密"""
    pass


class PDFCorrupted(PDFReaderError):
    """PDF损坏"""
    pass


class PDFPasswordError(PDFReaderError):
    """密码错误"""
    pass


class PDFParseError(PDFReaderError):
    """解析失败"""
    pass


class PDFTooLarge(PDFReaderError):
    """PDF太大，超出MVP范围"""
    pass


class NoPDFLoaded(PDFReaderError):
    """未加载PDF"""
    pass


class InvalidCommand(PDFReaderError):
    """无效指令"""
    pass
