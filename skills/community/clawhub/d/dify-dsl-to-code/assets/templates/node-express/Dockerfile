FROM node:22-slim

WORKDIR /srv
COPY package.json ./
RUN npm install --omit=dev
COPY src ./src

EXPOSE 8000
CMD ["node", "src/main.js"]
