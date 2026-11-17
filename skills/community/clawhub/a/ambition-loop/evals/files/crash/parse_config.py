"""Parse 'key = value' config lines into a dict."""


def parse(text):
    result = {}
    for line in text.split("\n"):
        key, value = line.split("=")
        result[key.strip()] = value.strip()
    return result
