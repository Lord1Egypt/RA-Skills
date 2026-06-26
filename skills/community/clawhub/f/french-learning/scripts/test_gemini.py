import subprocess
import json

prompt = "Provide information for the French word/phrase: 'Bonjour' (English: 'Hello'). Output strictly in JSON format with exactly these three keys: 'chinese_translation', 'example_fr', 'example_cn'."
cmd_gemini = ["gemini", "ask", prompt, "--json"]
res_gemini = subprocess.run(cmd_gemini, capture_output=True, text=True)
print(res_gemini.stdout)
