# n8n Node Development Guidelines - Research Findings

## Overview from Official Documentation

The official n8n documentation provides comprehensive guidance for building custom nodes. The main sections include:

### Prerequisites
- Some familiarity with JavaScript and TypeScript
- Ability to manage your own development environment, including git
- Knowledge of npm, including creating and submitting packages
- Familiarity with n8n, including understanding of data structures and item linking

### Main Documentation Sections
1. **Planning your build** - including which style to use
2. **Tutorials** - for different node building styles
3. **Testing your node** - including node linter and troubleshooting
4. **Sharing your node** - community submission, verification by n8n, or private use
5. **Reference material** - UI elements and file structure information

### Key Resources Found
- Main documentation: https://docs.n8n.io/integrations/creating-nodes/overview/
- Build guide: https://docs.n8n.io/integrations/creating-nodes/build/
- Development environment setup: https://docs.n8n.io/integrations/creating-nodes/build/node-development-environment/
- Starter repository: https://github.com/n8n-io/n8n-nodes-starter
- Community nodes guidelines: https://docs.n8n.io/integrations/community-nodes/build-community-nodes/




## Node Types

n8n supports two main node types:

### 1. Trigger Nodes
Trigger nodes start a workflow and supply the initial data. A workflow can contain multiple trigger nodes but with each execution, only one will execute, depending on the triggering event.

**Three types of trigger nodes:**

| Type | Description | Example Nodes |
|------|-------------|---------------|
| **Webhook** | Nodes for services that support webhooks. These nodes listen for events and trigger workflows in real time. | Zendesk Trigger, Telegram Trigger, Brevo Trigger |
| **Polling** | Nodes for services that don't support webhooks. These nodes periodically check for new data, triggering workflows when they detect updates. | Airtable Trigger, Gmail Trigger, Google Sheet Trigger, RssFeed Read Trigger |
| **Others** | Nodes that handle real-time responses not related to HTTP requests or polling. This includes message queue nodes and time-based triggers. | AMQP Trigger, RabbitMQ Trigger, MQTT Trigger, Schedule Trigger, Email Trigger (IMAP) |

### 2. Action Nodes
Action nodes perform operations as part of your workflow. These can include manipulating data, and triggering events in other systems.

## Node Building Styles

n8n has two node-building styles: **declarative** and **programmatic**.

### Declarative Style (Recommended for Most Nodes)
**Use declarative style for most nodes. This style:**
- Uses a JSON-based syntax, making it simpler to write, with less risk of introducing bugs
- Is more future-proof
- Supports integration with REST APIs

### Programmatic Style (Required for Specific Cases)
**You must use the programmatic style for:**
- Trigger nodes
- Any node that isn't REST-based (includes nodes that need to call a GraphQL API and nodes that use external dependencies)
- Any node that needs to transform incoming data
- Full versioning

### Key Differences

**Data Handling:**
- **Programmatic style:** Requires an `execute()` method, which reads incoming data and parameters, then builds a request
- **Declarative style:** Handles this using the `routing` key in the `operations` object

**Syntax Examples:**

**Programmatic Style Structure:**
```typescript
import {
    IExecuteFunctions,
    INodeExecutionData,
    INodeType,
    INodeTypeDescription,
    IRequestOptions,
} from 'n8n-workflow';

export class FriendGrid implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'FriendGrid',
        name: 'friendGrid',
        // ... properties configuration
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[]> {
        let responseData;
        const resource = this.getNodeParameter('resource', 0) as string;
        const operation = this.getNodeParameter('operation', 0) as string;
        
        // Manual request building and execution
        const options: IRequestOptions = {
            headers: {
                'Accept': 'application/json',
                'Authorization': `Bearer ${credentials.apiKey}`,
            },
            method: 'PUT',
            body: { contacts: [data] },
            url: 'https://api.sendgrid.com/v3/marketing/contacts',
            json: true,
        };
        responseData = await this.helpers.httpRequest(options);
        
        return [this.helpers.returnJsonArray(responseData)];
    }
}
```

**Declarative Style Structure:**
```typescript
import { INodeType, INodeTypeDescription } from 'n8n-workflow';

export class FriendGrid implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'FriendGrid',
        name: 'friendGrid',
        // Set up the basic request configuration
        requestDefaults: {
            baseURL: 'https://api.sendgrid.com/v3/marketing'
        },
        properties: [
            // ... resource and operation configuration
            {
                name: 'Create',
                value: 'create',
                description: 'Create a contact',
                // Add the routing object
                routing: {
                    request: {
                        method: 'POST',
                        url: '=/contacts',
                    },
                },
            },
        ],
    };
}
```

The declarative style uses the `routing` object to automatically handle request building, while the programmatic style requires manual implementation of the `execute()` method.


## Development Environment Setup

### Requirements
To build and test a node, you need:

1. **Node.js and npm**
   - Minimum version: Node 18.17.0 (recommended: Node 20+)
   - Installation options:
     - Use nvm (Node Version Manager) for Linux, Mac, and WSL
     - For Windows: Follow Microsoft's guide to Install NodeJS on Windows

2. **Local n8n instance**
   - Install with: `npm install n8n -g`
   - Follow the steps in "Run your node locally" to test your node

3. **Git**
   - Required to clone and use the n8n-node-starter repository

### Recommended Editor Setup
**n8n recommends using VS Code as your editor.**

**Required VS Code Extensions:**
- **ESLint** - For code linting and error detection
- **EditorConfig** - For consistent code formatting
- **Prettier** - For code formatting

By using VS Code and these extensions, you get access to the n8n node linter's warnings as you code.

## Community Node Standards

### Package Requirements
To make your node available to the n8n community node repository, you must:

1. **Package Naming Convention**
   - Package name must start with `n8n-nodes-` or `@<scope>/n8n-nodes-`
   - Examples: `n8n-nodes-weather` or `@weatherPlugins/n8n-nodes-weather`

2. **Package Keywords**
   - Include `n8n-community-node-package` in your package keywords

3. **Package.json Configuration**
   - Add your nodes and credentials to the `package.json` file inside the `n8n` attribute
   - Refer to the package.json in the starter node for an example

4. **Quality Assurance**
   - Check your node using the linter
   - Test it locally to ensure it works
   - Submit the package to the npm registry

### Verification Requirements for n8n Community Nodes

For nodes to be verified and discoverable in the n8n nodes panel, they must meet additional standards:

1. **Technical Guidelines**
   - Follow the technical guidelines for verified community nodes
   - All automated checks must pass
   - **No run-time dependencies allowed** for verified community nodes

2. **UX Guidelines**
   - Follow the UX guidelines for consistent user experience

3. **Documentation**
   - Appropriate documentation in the form of a README in the npm package or related public repository

4. **Submission Process**
   - Submit your node to npm first
   - n8n will fetch it from there for final vetting
   - Submit for verification through the official n8n process

## n8n Node Starter Repository

The official starter repository (https://github.com/n8n-io/n8n-nodes-starter) provides:

### What's Included
- Example nodes to help you get started
- Node linter and other dependencies
- Proper project structure and configuration
- Example credentials handling

### Basic Development Workflow

1. **Setup**
   - Generate a new repository from the template
   - Clone your new repo: `git clone https://github.com/<your-org>/<your-repo>.git`
   - Run `npm i` to install dependencies

2. **Development**
   - Browse examples in `/nodes` and `/credentials`
   - Modify examples or replace with your own nodes
   - Update the `package.json` to match your details

3. **Quality Control**
   - Run `npm run lint` to check for errors
   - Run `npm run lintfix` to automatically fix errors when possible
   - Test your node locally

4. **Documentation and Publishing**
   - Replace README with documentation for your node
   - Use the README_TEMPLATE to get started
   - Update the LICENSE file to use your details
   - Publish your package to npm

## Best Practices Summary

### Planning Phase
1. **Choose the right node type** (Trigger vs Action)
2. **Select appropriate building style** (Declarative vs Programmatic)
3. **Plan your UI design** following UX principles
4. **Determine file structure** based on complexity

### Development Phase
1. **Use the starter repository** for proper setup
2. **Follow naming conventions** for community compatibility
3. **Implement proper error handling** and validation
4. **Use the node linter** throughout development
5. **Test thoroughly** in local n8n instance

### Quality Assurance
1. **Follow technical guidelines** for verification
2. **Adhere to UX guidelines** for consistency
3. **Provide comprehensive documentation**
4. **Test all functionality** before submission

### Deployment
1. **Submit to npm registry** first
2. **Apply for verification** if seeking community visibility
3. **Maintain and update** based on feedback

## Key Resources

- **Main Documentation**: https://docs.n8n.io/integrations/creating-nodes/overview/
- **Starter Repository**: https://github.com/n8n-io/n8n-nodes-starter
- **Community Guidelines**: https://docs.n8n.io/integrations/community-nodes/build-community-nodes/
- **Development Environment**: https://docs.n8n.io/integrations/creating-nodes/build/node-development-environment/
- **Reference Materials**: https://docs.n8n.io/integrations/creating-nodes/build/reference/

This comprehensive guide ensures that n8n nodes are built to 100% compliance with official n8n guidelines and standards.

