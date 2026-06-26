from .auth import Authentication
from .note import Note

class APIModule:
    def __init__(self, __session):
        self.auth = Authentication(__session)
        self.note = Note(__session)
