import sys
import os

# Add src folder to the path to prioritize our local modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from cli import main

if __name__ == "__main__":
    main()
