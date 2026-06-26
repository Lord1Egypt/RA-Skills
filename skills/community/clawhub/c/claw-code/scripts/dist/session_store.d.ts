export interface StoredSession {
    readonly session_id: string;
    readonly messages: readonly string[];
    readonly input_tokens: number;
    readonly output_tokens: number;
}
export declare function loadSession(_sessionId: string): StoredSession;
export declare function saveSession(_session: StoredSession): string;
