export interface Logger {
    debug(message: string, ...args: any[]): void;
    info(message: string, ...args: any[]): void;
    warn(message: string, ...args: any[]): void;
    error(message: string, ...args: any[]): void;
}

export interface PromptContext {
    agentId: string;
    mode: 'full' | 'minimal' | 'code' | 'architect';
    workspaceDir: string;
    runtime?: {
        os: string;
        time: string;
        model: string;
    };
    state: Record<string, any>;
    tools?: ToolDefinition[];
    history?: string;
    logger?: Logger;
}

export interface ToolDefinition {
    type: string;
    function: {
        name: string;
        description?: string;
        parameters: {
            type: string;
            properties: Record<string, any>;
            required: string[];
        };
        script?: (parameters: any, context: any) => Promise<any>;
    };
}

export interface PromptTemplate {
    name: string;
    system: string; // Or a builder function? For now, keep as string template
    user: string;
    requestFormat: Record<string, string>;
    responseFormat?: Record<string, any> | 'text';
    tools?: Array<string | ToolDefinition>;
    then?: Record<string, {
        prompt?: string;
        function?: string;
        arguments: any;
    }>;
}

export interface AIProvider {
    name: string;
    url: string;
    headers: Record<string, string>;
    requestObject: {
        getMessage: (message: any) => { role: string; content: string | { type: string; text: string } };
        getOptions: (options: any) => Record<string, any>;
    };
    request: (request: any) => any;
    toolFormat: {
        formatTools: (tools: any[]) => any[];
        formatTool?: (tool: any) => any;
    };
    responseFormat: {
        getContent: (response: any) => string | undefined;
        getToolCall: (response: any) => any;
    };
}

export interface PromptEngineConfig {
    providers: AIProvider[];
    defaultProvider?: string;
    tools: ToolDefinition[];
    prompts: PromptTemplate[];
}

export interface RunnerOptions {
    maxDepth?: number;
    timeout?: number;
    retryAttempts?: number;
    retryDelay?: number;
    defaultProvider?: string;
    cycleProviders?: boolean;
    state?: Record<string, any>;
}
