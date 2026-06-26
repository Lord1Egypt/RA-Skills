# Browser Relay Commands

## Runtime

```bash
npx browser-relay-cli version
npx browser-relay-cli extension-path
npx browser-relay-cli relay-start
npx browser-relay-cli status
```

## Tabs

```bash
npx browser-relay-cli list-tabs
npx browser-relay-cli create-tab https://example.com
npx browser-relay-cli activate 123456
npx browser-relay-cli navigate 123456 https://news.ycombinator.com
```

## DOM-first actions

```bash
npx browser-relay-cli click 123456 'button'
npx browser-relay-cli hover 123456 'a'
npx browser-relay-cli type 123456 'input[name="q"]' 'search text'
npx browser-relay-cli press 123456 Enter
npx browser-relay-cli wait-for-selector 123456 'article'
npx browser-relay-cli wait-for-text 123456 'Founder'
npx browser-relay-cli wait-for-url 123456 '/search'
npx browser-relay-cli scroll 123456 800
```

## Screenshot-guided actions

```bash
npx browser-relay-cli screenshot 123456
npx browser-relay-cli describe-visible 123456
npx browser-relay-cli viewport 123456
npx browser-relay-cli click-at 123456 600 301
npx browser-relay-cli click-at-norm 123456 0.39 0.44
npx browser-relay-cli hover-at 123456 941 290
```

## Raw passthrough

```bash
npx browser-relay-cli raw BrowserRelay.getText '{"tabId":123456,"selector":"body"}'
npx browser-relay-cli raw CDP.send '{"tabId":123456,"method":"Runtime.evaluate","params":{"expression":"document.title","returnByValue":true}}'
```
