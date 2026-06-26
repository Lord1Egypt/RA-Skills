class PolicyExecutor:
    """
    Policy-guarded local executor.
    This is not OS-level sandboxing. It provides local policy checks only.
    """
    def __init__(self, allow_network=False):
        self.allow_network = allow_network

    def verify_callable(self, func):
        if not callable(func):
            raise TypeError("Provided tool is not callable")
        return True

    def execute(self, func, *args, **kwargs):
        self.verify_callable(func)
        return func(*args, **kwargs)
