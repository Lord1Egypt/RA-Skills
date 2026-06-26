import argparse
import os

from openai import OpenAI


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="qwen3.6-plus")
    parser.add_argument("--message", type=str, default="你是谁？")
    return parser.parse_args()


def main():
    args = get_args()
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(model=args.model, messages=[{"role": "user", "content": args.message}])
    print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
