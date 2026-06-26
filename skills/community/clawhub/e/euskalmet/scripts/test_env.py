from dotenv import load_dotenv
import os

load_dotenv()
pk = os.environ.get("EUSKALMET_API_PRIVATE_KEY")
if pk:
    print(f"FOUND: Starts with {pk[:30]}...")
    print(f"Line count: {len(pk.splitlines())}")
else:
    print("NOT FOUND")
