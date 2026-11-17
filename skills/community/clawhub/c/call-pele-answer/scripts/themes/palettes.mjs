// palettes — what the 调色器 (palette picker) offers. Two kinds, both plain data:
import { DEFAULT_KINDS } from './annotate-ui.mjs';
//   page    a whole-page preset: token overrides for light and dark. 墨纸 is the theme itself (no overrides).
//   swatch  one hue as a three-band ramp {l, m, d} (light / mid / dark). Put on a
//           component, it re-tints that component only: m → accent and first series, l → its surfaces,
//           d → its surfaces in dark mode. Ink stays the page ink, so text contrast never depends on the pick.
// Plugins add more with api.palette({...}); later registration of the same name wins.
const page = (name, label, light, dark, note) => ({ kind: 'page', name, label, light, dark, note });
const sw = (name, label, l, m, d) => ({ kind: 'swatch', name, label, l, m, d });
export default {
  name: 'builtin-palettes', apiVersion: 1,
  setup(api) {
    api.palette(page('ink', '墨纸', {}, {}, '墨与纸（默认）'));
    // warm paper, brown-black ink, five candy body colours
    api.palette(page('warm', '暖纸', {
      '--pe-paper': '#FBF5E9', '--pe-ink': '#231E16', '--pe-muted': '#6B6152', '--pe-faint': '#B9AE98', '--pe-border': '#E2D7C1',
      '--pe-surface': '#F4EBD8', '--pe-surface-2': '#EBDFC6',
      '--pe-blue': '#5A82C6', '--pe-red': '#CF5038', '--pe-yellow': '#B8860F', '--pe-green': '#3E8E66',
      '--pe-orange': '#E07A3F', '--pe-cyan': '#41538F', '--pe-purple': '#8A6BB8', '--pe-magenta': '#D8869C', '--pe-accent': '#CF5038',
    }, {
      '--pe-paper': '#1D1A15', '--pe-ink': '#EDE3D0', '--pe-muted': '#A89C86', '--pe-faint': '#5E5647', '--pe-border': '#3A342A',
      '--pe-surface': '#26221B', '--pe-surface-2': '#302A21',
      '--pe-blue': '#76A0E2', '--pe-red': '#EF6A4C', '--pe-yellow': '#F4B829', '--pe-green': '#93D3B0',
      '--pe-orange': '#F2955F', '--pe-cyan': '#8C9BD6', '--pe-purple': '#B9A0E0', '--pe-magenta': '#F3A6BB', '--pe-accent': '#EF6A4C',
    }, '暖纸与五色'));
    api.palette(page('blueprint', '蓝图', {
      '--pe-paper': '#F3F6FA', '--pe-ink': '#13233D', '--pe-muted': '#5A6B85', '--pe-faint': '#A9B6C9', '--pe-border': '#CBD5E3',
      '--pe-surface': '#E7EDF5', '--pe-surface-2': '#DAE3EF', '--pe-blue': '#2F5FB3', '--pe-accent': '#2F5FB3',
    }, {
      '--pe-paper': '#0E1A2E', '--pe-ink': '#D6E2F3', '--pe-muted': '#8DA0BC', '--pe-faint': '#43567A', '--pe-border': '#25395C',
      '--pe-surface': '#14233D', '--pe-surface-2': '#1B2D4C', '--pe-blue': '#6E9BE6', '--pe-accent': '#6E9BE6',
    }, '图纸风'));
    for (const s of [
      sw('tomato', '番茄', '#EF6A4C', '#CF5038', '#4A2219'),
      sw('mustard', '芥末', '#F4B829', '#B8860F', '#4E4A18'),
      sw('mint', '薄荷', '#93D3B0', '#3E8E66', '#1F4034'),
      sw('cobalt', '钴蓝', '#76A0E2', '#5A82C6', '#1C2948'),
      sw('blush', '腮红', '#F3A6BB', '#C26A84', '#4B2430'),
      sw('cyan', '青', '#8FCFC7', '#24837B', '#173B38'),
      sw('purple', '紫', '#C2B4E6', '#5E409D', '#2A2045'),
      sw('graphite', '石墨', '#D8D6CC', '#6F6E69', '#2A2927'),
    ]) api.palette(s);
    for (const k of DEFAULT_KINDS) api.annotation(k);
  },
};
