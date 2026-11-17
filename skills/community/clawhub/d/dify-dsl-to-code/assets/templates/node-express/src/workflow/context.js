/**
 * Variable pool and Dify template resolution.
 * Engine file — copy as-is from the skill template; do NOT edit per project.
 * Resolves Dify's {{#node_id.var#}}, {{#env.NAME#}}, {{#secret.NAME#}} syntax.
 */

const VAR_RE = /\{\{\s*#([^#]+)#\s*\}\}/g;

export class VariablePool {
  constructor() {
    /** @type {Map<string, any>} key = `${node_id}${var_name}` */
    this._data = new Map();
  }

  set(nodeId, varName, value) {
    this._data.set(`${nodeId} ${varName}`, value);
  }

  get(nodeId, varName, defaultValue = null) {
    const key = `${nodeId} ${varName}`;
    return this._data.has(key) ? this._data.get(key) : defaultValue;
  }

  setMany(nodeId, outputs) {
    for (const [k, v] of Object.entries(outputs || {})) this.set(nodeId, k, v);
  }

  resolveRef(ref) {
    ref = ref.trim();
    if (ref.startsWith('env.') || ref.startsWith('secret.')) {
      return process.env[ref.slice(ref.indexOf('.') + 1)] ?? '';
    }
    if (ref === 'context') return this.get('__runtime__', 'context', '');
    if (!ref.includes('.')) return this.get('sys', ref, '');
    const dot = ref.indexOf('.');
    return this.get(ref.slice(0, dot), ref.slice(dot + 1), '');
  }

  /** Interpolate all {{#...#}} placeholders in a string. Non-strings pass through. */
  resolve(text) {
    if (typeof text !== 'string') return text;
    return text.replace(VAR_RE, (_m, ref) => {
      const val = this.resolveRef(ref);
      return val == null ? '' : String(val);
    });
  }

  /** Recursively resolve placeholders in object/array/string structures. */
  resolveMap(obj) {
    if (Array.isArray(obj)) return obj.map((v) => this.resolveMap(v));
    if (obj && typeof obj === 'object') {
      return Object.fromEntries(Object.entries(obj).map(([k, v]) => [k, this.resolveMap(v)]));
    }
    return this.resolve(obj);
  }
}
