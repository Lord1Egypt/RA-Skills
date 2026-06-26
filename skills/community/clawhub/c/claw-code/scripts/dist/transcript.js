// Transcript – conversation transcript store (stub)
// Mirrored from Python src/transcript.py
export class TranscriptStore {
    constructor(entries = [], flushed = false) {
        this.entries = entries;
        this.flushed = flushed;
    }
    append(_message) {
        this.entries = [...this.entries, _message];
    }
    compact(_keepLast) {
        this.entries = this.entries.slice(-_keepLast);
    }
    replay() {
        return this.entries;
    }
    flush() {
        this.flushed = true;
    }
}
