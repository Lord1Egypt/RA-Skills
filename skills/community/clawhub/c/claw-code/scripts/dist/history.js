// History – session history log mirrored from Python src/history.py
export class HistoryLog {
    constructor() {
        this._events = [];
    }
    add(title, detail) {
        this._events.push({ title, detail });
    }
    get events() {
        return this._events;
    }
    asMarkdown() {
        const lines = ['# Session History', ''];
        for (const event of this._events) {
            lines.push(`- ${event.title}: ${event.detail}`);
        }
        return lines.join('\n');
    }
}
