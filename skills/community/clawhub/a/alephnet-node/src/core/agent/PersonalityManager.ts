import { PromptEngine } from './prompt-engine/PromptEngine';
import { promptRegistry } from './prompt-engine/PromptRegistry';
import { AIProvider, ToolDefinition } from './prompt-engine/types';

export interface Personality {
    id: string;
    name: string;
    description: string;
    systemPrompt: string;
    traits: string[];
    capabilities: string[];
    contextScope: string;
    intentKeywords?: string[];
}

export interface InteractionMetadata {
    conversationId?: string;
    personalityId?: string;
    providerId?: string;
    model?: string;
    [key: string]: any;
}

export interface InteractionResponse {
    content: string;
    model: string;
    providerId: string;
    usage?: any;
}

/**
 * PersonalityManager (Node Version)
 * 
 * Manages AI personalities and orchestrates interactions using the PromptEngine.
 * Unlike the client version, this does not depend on UI state managers.
 */
export class PersonalityManager {
    private personalities: Map<string, Personality> = new Map();
    private providers: AIProvider[] = [];
    private defaultProviderId: string = 'default';

    constructor(providers: AIProvider[], defaultProviderId?: string) {
        this.providers = providers;
        if (defaultProviderId) {
            this.defaultProviderId = defaultProviderId;
        } else if (providers.length > 0) {
            this.defaultProviderId = providers[0].name;
        }
    }

    public registerPersonality(personality: Personality) {
        this.personalities.set(personality.id, personality);
    }

    public getPersonality(id: string): Personality | undefined {
        return this.personalities.get(id);
    }

    /**
     * Handle an interaction with a specific personality.
     * 
     * @param content User input
     * @param metadata Context metadata
     * @param contextRetriever Optional function to fetch history/context string
     */
    public async handleInteraction(
        content: string, 
        metadata: InteractionMetadata,
        contextRetriever?: () => Promise<string>
    ): Promise<InteractionResponse> {
        
        // 1. Resolve Personality
        let personality: Personality | undefined;
        if (metadata.personalityId) {
            personality = this.getPersonality(metadata.personalityId);
        }

        // Default system prompt if no personality found
        const systemPrompt = personality ? personality.systemPrompt : "You are a helpful AI assistant.";

        // 2. Resolve Context
        const situationalContext = contextRetriever ? await contextRetriever() : '';

        // 3. Setup Prompt Engine
        const promptName = `personality-chat-${Date.now()}`;
        
        // Register ad-hoc template
        promptRegistry.register({
            name: promptName,
            system: '{corePersonality}\n\n{situationalContext}',
            user: '{userMessage}',
            requestFormat: { corePersonality: 'string', situationalContext: 'string', userMessage: 'string' },
            responseFormat: 'text'
        });

        const tools: ToolDefinition[] = []; // Add default node tools here if needed

        const engine = new PromptEngine({
            providers: this.providers,
            tools: tools,
            prompts: [],
            defaultProvider: metadata.providerId || this.defaultProviderId
        });

        // 4. Execute
        const result = await engine.execute(promptName, {
            corePersonality: systemPrompt,
            situationalContext: situationalContext,
            userMessage: content
        }, {
            defaultProvider: metadata.providerId || this.defaultProviderId,
            state: { ...metadata }
        });

        return {
            content: result.text,
            model: metadata.model || 'unknown',
            providerId: metadata.providerId || this.defaultProviderId,
            usage: result.raw?.usage
        };
    }
}
