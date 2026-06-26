// stealth.js — Fusion Search anti-detection initialization script
// Injected via Playwright context.add_init_script()

Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
Object.defineProperty(navigator, 'plugins', {
    get: () => [
        {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
        {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpafafjmlifpcpbgpcj'},
        {name: 'Native Client Executable', filename: 'internal-nacl-plugin'}
    ]
});
Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']});
Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
window.chrome = {runtime: {}};
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
        Promise.resolve({ state: Notification.permission }) :
        originalQuery(parameters)
);
const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
HTMLCanvasElement.prototype.toDataURL = function(type) {
    if (type === 'image/png' && this.width === 220 && this.height === 30) {
        return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANwAAAAeCAYAAABwJ3rwAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAABmJLR0QA/wD/AP+gvaeTAAAABmJLR0QA/wD/AP+gvaeT';
    }
    return originalToDataURL.apply(this, arguments);
};
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    if (parameter === 37445) return 'Intel Inc.';
    if (parameter === 37446) return 'Intel Iris OpenGL Engine';
    return getParameter.apply(this, arguments);
};
