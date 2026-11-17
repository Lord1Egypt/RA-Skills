"""Test-only lifecycle smoke workload; not a scientific experiment or benchmark."""
from axiotic_experiments.runtime import EnvironmentRun

def main():
    with EnvironmentRun() as run:
        run.log({"test_only/ok": 1}, step=0)

if __name__ == "__main__":
    main()
