export interface HistoryEvent {
    readonly title: string;
    readonly detail: string;
}
export declare class HistoryLog {
    private readonly _events;
    add(title: string, detail: string): void;
    get events(): readonly HistoryEvent[];
    asMarkdown(): string;
}
