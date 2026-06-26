// agent-system plugin entry point
import { orchestrator, executor, reviewer, evolve, tokenControl, dispatch } from './src/orchestrator.js';

export default {
    name: 'agent-system',
    version: '1.0.0',
    
    tools: {
        agent_dispatch: async (input) => {
            const result = await dispatch(input);
            return JSON.parse(result);
        },
        
        agent_plan: async (input) => {
            const result = orchestrator(input);
            return JSON.parse(result);
        },
        
        agent_review: async (input) => {
            const result = reviewer(input);
            return JSON.parse(result);
        }
    }
};
