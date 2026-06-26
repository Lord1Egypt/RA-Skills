/**
 * ChannelBridge — Cross-Platform Message Routing
 * @author @TheShadowRose
 * @license MIT
 */

class ChannelBridge {
  constructor(options = {}) {
    this.routes = options.routes || [];
    this.transforms = { forward: m => m, summarize: m => ({ ...m, body: (m.body || '').substring(0, 200) + '...' }), digest: null };
    this.buffer = {};
  }

  addRoute(route) {
    this.routes.push({
      name: route.name || 'unnamed',
      from: Array.isArray(route.from) ? route.from : [route.from],
      to: Array.isArray(route.to) ? route.to : [route.to],
      filter: route.filter || null,
      transform: route.transform || 'forward',
      schedule: route.schedule || null
    });
    return this;
  }

  process(message) {
    const results = [];
    for (const route of this.routes) {
      if (!route.from.includes(message.platform)) continue;
      if (route.filter && !this._matchFilter(message, route.filter)) continue;
      if (route.schedule) { this._bufferForDigest(route.name, message); continue; }

      const transform = this.transforms[route.transform] || this.transforms.forward;
      const transformed = transform(message);

      for (const dest of route.to) {
        results.push({ route: route.name, destination: dest, message: transformed });
      }
    }
    return results;
  }

  getDigest(routeName) {
    const messages = this.buffer[routeName] || [];
    this.buffer[routeName] = [];
    return {
      route: routeName,
      count: messages.length,
      messages,
      summary: `${messages.length} messages buffered for digest`
    };
  }

  _matchFilter(message, filter) {
    const text = ((message.body || '') + ' ' + (message.subject || '')).toLowerCase();
    const from = (message.from || '').toLowerCase();
    if (filter.includes('contains:')) {
      const term = filter.split('contains:')[1].split(' ')[0].toLowerCase();
      if (text.includes(term)) return true;
    }
    if (filter.includes('from:')) {
      const sender = filter.split('from:')[1].split(' ')[0].toLowerCase();
      if (from.includes(sender)) return true;
    }
    // Unknown filter types pass through (don't silently drop messages)
    if (!filter.includes('contains:') && !filter.includes('from:')) return true;
    return false;
  }

  _bufferForDigest(routeName, message) {
    if (!this.buffer[routeName]) this.buffer[routeName] = [];
    this.buffer[routeName].push(message);
  }
}

module.exports = { ChannelBridge };
