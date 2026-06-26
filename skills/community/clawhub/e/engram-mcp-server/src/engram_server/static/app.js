// Engram UI — Alpine.js application

function app() {
  return {
    view: 'list',
    search: '',
    engrams: [],
    currentEngram: null,
    files: [],
    activeFile: null,
    fileContent: '',
    dirty: false,
    stats: null,
    toast: null,

    async init() {
      await this.loadEngrams();
    },

    get filteredEngrams() {
      if (!this.search) return this.engrams;
      const q = this.search.toLowerCase();
      return this.engrams.filter(e =>
        e.name.toLowerCase().includes(q) ||
        (e.description || '').toLowerCase().includes(q) ||
        (e.tags || []).some(t => t.toLowerCase().includes(q))
      );
    },

    async loadEngrams() {
      try {
        const res = await fetch('/api/engrams');
        this.engrams = await res.json();
      } catch (e) {
        this.showToast('加载失败', 'error');
      }
    },

    async selectEngram(name) {
      try {
        const [infoRes, filesRes] = await Promise.all([
          fetch(`/api/engrams/${name}`),
          fetch(`/api/engrams/${name}/files`),
        ]);
        this.currentEngram = await infoRes.json();
        this.files = await filesRes.json();
        this.activeFile = null;
        this.fileContent = '';
        this.dirty = false;
        this.view = 'detail';
      } catch (e) {
        this.showToast('加载 Engram 失败', 'error');
      }
    },

    async openFile(path) {
      if (this.dirty && !confirm('当前文件未保存，确定切换？')) return;
      try {
        const name = this.currentEngram.name;
        const res = await fetch(`/api/engrams/${name}/files/${path}`);
        this.fileContent = await res.text();
        this.activeFile = path;
        this.dirty = false;
      } catch (e) {
        this.showToast('读取文件失败', 'error');
      }
    },

    async saveFile() {
      try {
        const name = this.currentEngram.name;
        const res = await fetch(`/api/engrams/${name}/files/${this.activeFile}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: this.fileContent }),
        });
        const data = await res.json();
        if (data.ok) {
          this.dirty = false;
          this.showToast('已保存', 'success');
        } else {
          this.showToast(data.error || '保存失败', 'error');
        }
      } catch (e) {
        this.showToast('保存失败', 'error');
      }
    },

    showToast(msg, type = 'info') {
      this.toast = { msg, type };
      setTimeout(() => { this.toast = null; }, 2500);
    },

    async loadStats() {
      try {
        const res = await fetch('/api/stats');
        this.stats = await res.json();
      } catch (e) {
        this.showToast('统计加载失败', 'error');
      }
    },
  };
}
