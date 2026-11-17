# SOURCE OF TRUTH for the image. `scripts/setup.sh` copies this to ./Dockerfile on
# every build, and the generated copy is gitignored. The .sh extension is required
# because clawhub only bundles files with known text extensions, and `Dockerfile`
# has none. Edit this file, never the generated one.
#
# The Playwright version MUST match the base image tag. `playwright: "^1.40.0"`
# plus a bare `npm install` let the client float to a release whose expected
# browser build is not the one baked into this image.
ARG PLAYWRIGHT_VERSION=1.40.0
FROM mcr.microsoft.com/playwright:v${PLAYWRIGHT_VERSION}-jammy

ARG PLAYWRIGHT_VERSION
WORKDIR /app

COPY package.json package-lock.json* ./
# Prefer the lockfile when present so builds are reproducible.
RUN if [ -f package-lock.json ]; then npm ci --omit=dev; \
    else npm install --omit=dev --no-audit --no-fund; fi \
    && npm ls playwright \
    && npm cache clean --force

# The base image already ships the matching browser build; re-downloading it only
# added image size and a second source of version drift.

COPY assets/ ./assets/
COPY scripts/ ./scripts/

# config/ is deliberately NOT copied. Baking proxies.json in put live credentials
# into an image layer, where they survive deletion and are readable by anyone who
# can pull or `docker save` the image. Supply credentials at run time instead:
#   docker run --rm -e AMAZON_PROXIES="http://user:pass@host:port" amazon-scraper ...
#   docker run --rm -v "$PWD/config/proxies.json:/app/config/proxies.json:ro" ...

RUN mkdir -p /data /app/config && chown -R pwuser:pwuser /data /app

# Don't run the browser as root.
USER pwuser

CMD ["node", "assets/amazon_handler.js"]
