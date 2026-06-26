FROM mcr.microsoft.com/playwright:v1.40.0-jammy

WORKDIR /app

COPY package.json ./
RUN npm install
RUN npx playwright install chromium

COPY assets/ ./assets/
COPY scripts/ ./scripts/
COPY config/ ./config/

RUN mkdir -p /data

CMD ["node", "assets/amazon_handler.js"]
