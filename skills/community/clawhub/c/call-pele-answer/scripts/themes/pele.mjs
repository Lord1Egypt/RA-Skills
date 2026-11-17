// pele — the default theme. ink on warm paper, one token
// set shared by prose and diagrams, flat at rest, a note-shaped single column. A theme is only tokens +
// CSS: forms bring their own component CSS, written against the --pe-* tokens, so any theme that
// defines those tokens styles every form, including forms from plugins.
import { readFileSync } from 'node:fs';
const css = readFileSync(new URL('./pele.css', import.meta.url), 'utf8');
export default {
  name: 'pele-theme', apiVersion: 1,
  setup(api) {
    api.theme({
      name: 'pele',
      describe: '墨与纸 · 单栏笔记 · 平放',
      tokens: ['--pe-paper', '--pe-ink', '--pe-muted', '--pe-faint', '--pe-border', '--pe-surface', '--pe-surface-2', '--pe-blue', '--pe-red', '--pe-green', '--pe-yellow', '--pe-orange', '--pe-cyan', '--pe-purple', '--pe-magenta', '--pe-accent', '--pe-font', '--pe-mono', '--pe-radius', '--pe-measure'],
      css,
    });
  },
};
