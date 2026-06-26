# Prompt Engine

The Prompt Engine is a sophisticated subsystem for managing and executing AI workflows. It provides a structured, modular way to define prompts, manage state, and execute multi-step tasks with tool integration.

## Features

- **PromptBuilder**: Dynamically construct system prompts with modular sections (Identity, Safety, Tooling, Context).
- **State Management**: Maintain conversation history and task state across multiple prompt executions.
- **Workflow Execution**: Define complex workflows with conditional logic (`then` transitions).
- **Tool Integration**: Seamlessly integrate tools into prompts and execute them automatically.
- **Structured I/O**: Define strict request and response formats using JSON schemas.

## Usage

### 1. Define a Prompt Template

```typescript
import { promptRegistry } from './src/core/prompt-engine';

promptRegistry.register({
    name: 'taskDecomposer',
    system: `You are a task decomposition expert. Break down the task into subtasks.`,
    user: `Task: {task}`,
    requestFormat: { task: 'string' },
    responseFormat: { subtasks: 'array' },
    then: {
        "subtasks.length > 0": {
            function: 'executeSubtasks',
            arguments: { subtasks: '{subtasks}' }
        }
    }
});
```

### 2. Execute a Prompt

```typescript
import { PromptEngine } from './src/core/prompt-engine';

const engine = new PromptEngine({
    providers: [/* configured providers */],
    tools: [/* available tools */]
});

const result = await engine.execute('taskDecomposer', { 
    task: 'Build a login page' 
});
```

## Architecture

- **PromptBuilder**: Handles the construction of the system prompt string, injecting safety rules, runtime context, and tool definitions.
- **PromptEngine**: The main orchestrator that manages the execution loop, state updates, and provider interactions.
- **PromptRegistry**: A central registry for storing and retrieving prompt templates.

## Logging

The engine supports a `Logger` interface for debugging. You can pass a logger instance in the `PromptContext` or rely on the default console logger.

```typescript
interface Logger {
    debug(message: string, ...args: any[]): void;
    info(message: string, ...args: any[]): void;
    warn(message: string, ...args: any[]): void;
    error(message: string, ...args: any[]): void;
}
```

## Testing

The engine is designed to be testable. You can mock the `AIProvider` to test prompt logic without making API calls.

```typescript
// Example test setup
const mockProvider = {
    // ... mock implementation
};
const engine = new PromptEngine({ providers: [mockProvider], ... });
```
