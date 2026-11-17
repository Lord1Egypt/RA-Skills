"""Small, injectable subprocess boundary used only for safe engine probing."""
from dataclasses import dataclass
import subprocess
import tempfile

from .errors import OCRError

@dataclass(frozen=True)
class ProcessResult:
    returncode: int
    stdout: str
    stderr: str

class ProcessRunner:
    def __init__(self, *, timeout: float = 5.0, max_output_bytes: int = 65536):
        self.timeout = timeout
        self.max_output_bytes = max_output_bytes

    def run(self, argv: list[str]) -> ProcessResult:
        if not argv or not all(isinstance(arg, str) for arg in argv):
            raise OCRError("probe argv must be a non-empty argument list", "OCR_PROVIDER_CONTRACT_INVALID")
        try:
            with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
                proc = subprocess.Popen(argv, shell=False, stdout=out, stderr=err,
                                        env={"PATH": "/usr/bin:/bin:/usr/local/bin"})
                try:
                    proc.wait(timeout=self.timeout)
                except subprocess.TimeoutExpired as exc:
                    proc.kill()
                    proc.wait()
                    raise OCRError("provider probe timed out", "OCR_PROVIDER_UNAVAILABLE") from exc
                out.seek(0); err.seek(0)
                stdout = out.read(self.max_output_bytes + 1)
                stderr = err.read(self.max_output_bytes + 1)
                if len(stdout) > self.max_output_bytes or len(stderr) > self.max_output_bytes:
                    raise OCRError("provider probe output exceeded limit", "OCR_PROVIDER_FAILED")
                return ProcessResult(proc.returncode, stdout.decode(errors="replace"), stderr.decode(errors="replace"))
        except FileNotFoundError as exc:
            raise OCRError("provider executable unavailable", "OCR_PROVIDER_UNAVAILABLE") from exc
        except OSError as exc:
            raise OCRError("provider probe unavailable", "OCR_PROVIDER_UNAVAILABLE") from exc
