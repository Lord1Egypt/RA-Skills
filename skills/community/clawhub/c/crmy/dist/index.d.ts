interface ToolDef {
    id: string;
    name: string;
    description: string;
    input: {
        type: 'object';
        properties: Record<string, {
            type: string;
            description: string;
            enum?: string[];
        }>;
        required?: string[];
    };
    handler: (input: Record<string, unknown>) => Promise<unknown>;
}
interface OpenClawApi {
    registerTool(tool: ToolDef): void;
    config?: {
        serverUrl?: string;
        apiKey?: string;
    };
    logger?: {
        info(msg: string): void;
        error(msg: string): void;
    };
}
declare const _default: (api: OpenClawApi) => void;

export { _default as default };
