# DashScope OpenAI Compatible-mode notes

Endpoint base URL:

- https://dashscope.aliyuncs.com/compatible-mode/v1

Auth:

- `Authorization: Bearer <api_key>`

This skill assumes an OpenAI Images API compatible endpoint at:

- `POST {baseUrl}/images/generations`

If DashScope returns a schema mismatch error, adjust `scripts/dashscope_image_gen.py` to the exact payload/route and keep this file updated.
