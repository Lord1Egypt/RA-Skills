# Excalidraw API snippets

## Find `excalidrawAPI` from excalidraw.com page runtime

```js
() => {
  const rootEl = document.querySelector('.excalidraw');
  const fiberKey = Object.getOwnPropertyNames(rootEl || {}).find(k => k.startsWith('__reactFiber$'));
  const root = rootEl?.[fiberKey];
  let api = null;
  const seen = new Set();

  (function walk(node) {
    if (!node || seen.has(node) || api) return;
    seen.add(node);
    const mp = node.memoizedProps;
    if (mp && mp.excalidrawAPI && typeof mp.excalidrawAPI.updateScene === 'function') {
      api = mp.excalidrawAPI;
      return;
    }
    walk(node.child);
    walk(node.sibling);
  })(root);

  if (!api) return { ok: false, reason: 'no api' };
  return { ok: true, methods: Object.keys(api) };
}
```

## Apply scene elements

```js
(elements) => {
  const rootEl = document.querySelector('.excalidraw');
  const fiberKey = Object.getOwnPropertyNames(rootEl || {}).find(k => k.startsWith('__reactFiber$'));
  const root = rootEl?.[fiberKey];
  let api = null;
  const seen = new Set();

  (function walk(node) {
    if (!node || seen.has(node) || api) return;
    seen.add(node);
    const mp = node.memoizedProps;
    if (mp && mp.excalidrawAPI && typeof mp.excalidrawAPI.updateScene === 'function') {
      api = mp.excalidrawAPI;
      return;
    }
    walk(node.child);
    walk(node.sibling);
  })(root);

  if (!api) return { ok: false, reason: 'no api' };

  api.updateScene({
    elements,
    appState: {
      ...api.getAppState(),
      showWelcomeScreen: false,
      viewBackgroundColor: '#f8f9fb'
    }
  });

  api.scrollToContent(elements, { fitToContent: true });
  return { ok: true, count: elements.length };
}
```
