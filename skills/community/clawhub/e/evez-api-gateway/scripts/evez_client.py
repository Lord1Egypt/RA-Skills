"""
EVEZ API Gateway — Python client wrapper
"""
import os
from openai import OpenAI

MODELS = {
    "smart": "evez-smart",
    "code": "evez-code",
    "fast": "evez-fast",
    "vision": "evez-vision",
}

BASE_URL = "https://evez-api2.fly.dev/v1"


class EvezClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("EVEZ_API_KEY", "")
        self.client = OpenAI(base_url=BASE_URL, api_key=self.api_key)

    def chat(self, message: str, model: str = "smart", system: str = None, stream: bool = False):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})

        model_id = MODELS.get(model, model)
        response = self.client.chat.completions.create(
            model=model_id, messages=messages, stream=stream
        )
        if stream:
            return response
        return response.choices[0].message.content

    def code(self, prompt: str, language: str = None):
        system = f"You are an expert programmer. Write clean, efficient code. Language: {language or 'auto-detect'}"
        return self.chat(prompt, model="code", system=system)

    def vision(self, text: str, image_url: str):
        response = self.client.chat.completions.create(
            model="evez-vision",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }]
        )
        return response.choices[0].message.content

    def models(self):
        return list(MODELS.items())


if __name__ == "__main__":
    key = os.environ.get("EVEZ_API_KEY")
    if not key:
        print("Set EVEZ_API_KEY env var (get one at https://evez-api2.fly.dev/signup)")
        exit(1)
    client = EvezClient(key)
    print(client.chat("Say hello in 5 words"))
