import mermaid from './mermaid.mjs';
import callout from './callout.mjs';
import steps from './steps.mjs';
import tabs from './tabs.mjs';
import slider from './slider.mjs';
import code from './code.mjs';
import views from './views.mjs';
export default { name: 'builtin-forms', apiVersion: 1, setup(api) { for (const f of [code, mermaid, callout, steps, tabs, slider, views]) api.form(f); } };
