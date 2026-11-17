FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn web3 python-dotenv

COPY server-v5.py .

EXPOSE 4022

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:4022/health')" || exit 1

CMD ["python", "server-v5.py"]
