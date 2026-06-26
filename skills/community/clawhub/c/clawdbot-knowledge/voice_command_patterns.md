# Voice Command Patterns for DeepAllSpeak

Effective voice command design patterns for optimal DeepAllSpeak usage across all 20+ MCP servers and multi-agent systems.

## Table of Contents

1. [General Principles](#general-principles)
2. [Basic Command Categories](#basic-command-categories)
3. [Multi-Agent Commands](#multi-agent-commands)
4. [Workflow Automation Commands](#workflow-automation-commands)
5. [Document Intelligence Commands](#document-intelligence-commands)
6. [Desktop & Browser Automation](#desktop--browser-automation)
7. [Self-Memory System Commands](#self-memory-system-commands)
8. [Advanced Multi-Tool Workflows](#advanced-multi-tool-workflows)
9. [Language Support](#language-support)
10. [Best Practices](#best-practices)

---

## General Principles

### 1. Be Specific and Clear

```
✅ Good:
- "Create a new file called config.json in the project directory"
- "Search my emails from John about the Q3 proposal"
- "Upload the PDF report.pdf from Downloads to DeepALL document intelligence"
- "Use FATONI Code Agent to generate a REST API in Python"

❌ Avoid:
- "Do that file thing"
- "Find that email"
- "Process the document"
- "Generate some code"
```

### 2. Use Action Verbs

```
✅ Good Commands:
- Create, Upload, Search, Find, Delete, Update
- Analyze, Process, Convert, Extract
- Send, Fetch, Download, Save
- Generate, Review, Optimize, Test (for agents)
- Delegate, Orchestrate, Execute (for multi-agent)

Structure: [Action] [Object] [Details] [Agent/Tool (optional)]
Example: "Upload Q3_Report.pdf to DeepALL and analyze revenue trends"
```

### 3. Provide Context

```
✅ Good:
- "Search for Python files modified last week in the backend folder"
- "Query my sales documents about Q4 revenue trends with citations"
- "Create a summary of the meeting notes from yesterday using DeepSynaptica"
- "Use FATONI Strategy Agent to develop a go-to-market strategy"

❌ Too Vague:
- "Search for files"
- "Query documents"
- "Create summary"
- "Make a strategy"
```

### 4. Specify Agents When Needed

```
✅ Explicit Agent Selection:
- "Use FATONI Code Agent to generate this code"
- "Have DeepSynaptica analyze the cognitive phases in this text"
- "Delegate to Auggie: Refactor the authentication system"
- "Use FATONI Security Agent to scan for vulnerabilities"

✅ Implicit (AI selects best agent):
- "Generate Python code for a REST API"
  → AI chooses FATONI Code Agent
- "Analyze the document semantically"
  → AI chooses DeepSynaptica
- "Review this code for security issues"
  → AI chooses FATONI Security Agent
```

---

## Basic Command Categories

### File Operations

**Creating Files:**
```
"Create a new file called app.py in the src directory"
"Make a folder named tests in the current project"
"Generate a README file with project description"
"Write this JSON data to config.json in the project root"
```

**Reading/Searching Files:**
```
"Read the contents of config.json"
"Show me all TypeScript files in the components folder"
"Search for files containing the word 'authentication'"
"List all files in the Downloads directory"
```

**Modifying Files:**
```
"Add the line 'import pandas' to analysis.py"
"Replace 'localhost' with 'api.example.com' in config"
"Delete the temp folder and all its contents"
"Update the version number in package.json to 2.0.0"
```

### GitHub Operations

**Notifications & Issues:**
```
"List my GitHub notifications"
"Show me all open issues in the frontend repository"
"Create an issue titled 'Fix login bug' in the main repository"
"Close issue #42 in the backend repo"
```

**Pull Requests:**
```
"Show me all pull requests waiting for my review"
"Get details of pull request #15"
"List all my open pull requests"
```

**Repositories:**
```
"List my starred repositories"
"Show me the README of the react-boilerplate repository"
"Search for repositories about machine learning"
```

### Email Operations

**Reading Emails:**
```
"Check if I have any unread emails from support@company.com"
"Search my inbox for emails about the project proposal"
"Show me emails from last week"
```

**Sending Emails:**
```
"Send an email to team@company.com with subject 'Meeting Update'"
"Draft an email to john@example.com about the quarterly report"
```

---

## Multi-Agent Commands

### FATONI Code Agent (4 Tools)

**Code Generation:**
```
"Generate a Python function for calculating Fibonacci numbers"
"Create a React component for a user profile card"
"Write a SQL query to get top 10 customers by revenue"
"Generate a REST API endpoint for user authentication"
"Use FATONI to build a TypeScript class for data validation"
```

**Code Review:**
```
"Review this code for best practices"
"Check my Python script for code quality issues"
"Analyze this function and suggest improvements"
"Use FATONI Code Agent to review my pull request"
```

**Code Optimization:**
```
"Optimize this algorithm for better performance"
"Refactor this code to be more readable"
"Improve the efficiency of this database query"
"Suggest performance optimizations for this loop"
```

**Test Generation:**
```
"Generate unit tests for this function"
"Create test cases for the authentication module"
"Write integration tests for the API endpoints"
"Generate Jest tests for this React component"
```

### FATONI DeepALL CodeArchitect (7 Tools, GPT-4)

**Advanced Code Generation:**
```
"Use DeepALL GPT to generate a complete user authentication system"
"Create a full CRUD API with error handling and validation"
"Generate a microservice architecture for e-commerce"
```

**Code Explanation:**
```
"Explain how this algorithm works"
"Use DeepALL GPT to explain this complex codebase structure"
"Break down this regex pattern and explain each part"
```

**Commit Messages:**
```
"Generate a commit message for these changes"
"Create a conventional commit message for this feature"
"Use DeepALL GPT to write a descriptive commit message"
```

**Health Check:**
```
"Check if DeepALL GPT service is available"
"Verify GPT-4 connection status"
```

### FATONI Strategy Agent (2 Tools)

**Strategic Insights:**
```
"Analyze the competitive landscape for our product"
"Provide strategic insights on entering the European market"
"What are the key trends in AI for 2025?"
"Use FATONI Strategy Agent to evaluate this business opportunity"
```

**Strategy Development:**
```
"Develop a go-to-market strategy for our new SaaS product"
"Create a product roadmap for the next 6 months"
"Design a user acquisition strategy with limited budget"
"Build a competitive positioning strategy"
```

### FATONI Analytics Agent (2 Tools)

**Data Analysis:**
```
"Analyze user behavior from the last 30 days"
"Process this sales data and extract key insights"
"Identify trends in customer churn rates"
"Use FATONI Analytics to find patterns in this dataset"
```

**Dashboard Creation:**
```
"Create a dashboard for sales metrics"
"Build a real-time analytics dashboard for user activity"
"Generate a KPI dashboard with revenue, users, and conversion"
```

### FATONI Security Agent (2 Tools)

**Security Scanning:**
```
"Scan this code for security vulnerabilities"
"Check the authentication system for security flaws"
"Use FATONI Security Agent to analyze this API for vulnerabilities"
"Identify SQL injection risks in this code"
```

**Security Audits:**
```
"Perform a security audit on the entire codebase"
"Audit the user authentication flow for security issues"
"Review our API security posture"
"Generate a security report for the web application"
```

### FATONI Designer Agent (1 Tool)

**UI Component Design:**
```
"Design a card component for the dashboard"
"Create a React component for a pricing table"
"Generate a form component with validation"
"Use FATONI Designer to build a navigation menu component"
```

### FATONI Orchestration Agent

**Multi-Agent Coordination:**
```
"Orchestrate building a complete login system"
  → Code Agent: Generate code
  → Security Agent: Security review
  → Designer Agent: UI components
  → Analytics Agent: Add tracking

"Coordinate the agents to build a feature end-to-end"
```

### FATONI Web Agent (3 Tools)

**Web Scraping:**
```
"Scrape product prices from example.com"
"Extract all article titles from the news website"
"Use FATONI Web Agent to gather data from this URL"
```

**Web Search:**
```
"Search the web for latest AI research papers"
"Find recent articles about GPT-4"
"Search for tutorials on React hooks"
```

**API Calls:**
```
"Make an API call to the weather service for San Francisco"
"Query the GitHub API for trending repositories"
"Call the OpenAI API to generate a summary"
```

### DeepSynaptica AGI (9 Tools)

**Full Cognitive Processing:**
```
"Process this document through all cognitive phases"
"Use DeepSynaptica to analyze this text comprehensively"
"Apply full cognitive analysis to this research paper"
```

**Cognitive Phase Detection:**
```
"Detect the cognitive phases in this meeting transcript"
"Identify which phase of thinking this text represents"
"Analyze the cognitive flow in this essay"
```

**GPT-4 Agent Query:**
```
"Use DeepSynaptica GPT agent as an analyst to review this data"
"Query DeepSynaptica with the reflector role for meta-analysis"
"Use the strategist role to evaluate this plan"
```

**Knowledge Mapping:**
```
"Build a knowledge map of the uploaded research papers"
"Create a knowledge graph from these documents"
"Map the relationships between concepts in this text"
"Use DeepSynaptica to visualize the knowledge structure"
```

**Semantic Analysis:**
```
"Perform semantic document analysis on the contract"
"Analyze the semantic themes in this article"
"Extract semantic meaning from this technical document"
```

**Meta-Reflection:**
```
"Perform deep reflection on my decision-making process"
"Use DeepSynaptica to analyze my thought patterns"
"Reflect on the biases in this analysis"
```

**Trend Evaluation:**
```
"Evaluate meta trends across all my uploaded documents"
"Identify emerging patterns in the research literature"
"Analyze trend evolution over time"
```

**Vault History:**
```
"Show the vault history for this analysis"
"Retrieve historical cognitive processing data"
"Track how my thinking has evolved"
```

### Auggie (3 Tools with MCP Forwarding)

**Complex Task Delegation:**
```
"Delegate to Auggie: Refactor the authentication system and update tests"
"Have Auggie review the entire codebase and suggest improvements"
"Delegate to Auggie with filesystem and GitHub: Implement the new feature"
"Ask Auggie to fix the bug in the payment module"
```

**With MCP Server Forwarding:**
```
"Delegate to Auggie with filesystem and GitHub access:
 Refactor the auth system across multiple files"

"Have Auggie use filesystem, github, and memory tools to
 complete this multi-step refactoring"
```

**Status Check:**
```
"Check Auggie connection status"
"Verify Auggie capabilities"
"List available MCP servers for Auggie"
```

---

## Workflow Automation Commands

### n8n Workflow Automation (15+ Tools)

**Create Workflows:**
```
"Create an n8n workflow to monitor new emails and create Notion tasks"
"Build a workflow for syncing customer data between Salesforce and HubSpot"
"Generate an n8n workflow for daily sales report automation"
"Create a workflow to post new blog articles to social media"
```

**List & Manage Workflows:**
```
"List all my n8n workflows"
"Show me all active workflows"
"Get details of the customer-onboarding workflow"
"List workflows in the marketing category"
```

**Activate/Deactivate:**
```
"Activate the daily-report workflow"
"Deactivate the test-automation workflow"
"Pause the email-notification workflow"
```

**Execute Workflows:**
```
"Trigger the customer-onboarding workflow for john@example.com"
"Execute the data-sync workflow manually"
"Run the sales-report workflow with yesterday's data"
```

**Update Workflows:**
```
"Update the email workflow to add Slack notifications"
"Modify the data-sync workflow to run every hour"
"Change the trigger for the customer workflow to webhook"
```

**Delete Workflows:**
```
"Delete the old-test workflow"
"Remove the deprecated-sync workflow"
```

**Execution History:**
```
"Show executions of the customer-onboarding workflow"
"List failed workflow executions from last week"
"Get details of execution #12345"
```

**Node Generation:**
```
"Generate an email trigger node for n8n"
"Create a Slack notification action node"
"Build a data transformation node for JSON"
```

**Validation & Export:**
```
"Validate the sales-pipeline workflow"
"Export the customer-workflow to JSON"
"Export the data-sync workflow to PDF"
"Validate this workflow definition before creating it"
```

**Webhooks:**
```
"Create a webhook trigger for the order-processing workflow"
"Generate a webhook URL for external integrations"
```

### n8n + Multi-Agent Workflows

**Combined Patterns:**
```
"Create a workflow that:
 1. Triggers on new email
 2. Uses FATONI Analytics to analyze sentiment
 3. Routes to appropriate team based on analysis
 4. Creates GitHub issue if needed
 5. Sends Slack notification"

"Build an n8n workflow that:
 - Monitors customer feedback forms
 - Uses DeepSynaptica for semantic analysis
 - Categorizes by theme
 - Triggers FATONI Strategy Agent for insights
 - Updates dashboard"
```

---

## Document Intelligence Commands

### Document Upload & Processing

**Docling MCP (19 Tools):**
```
"Upload the Q3_Report.pdf from my Downloads folder"
"Process the quarterly-financials.docx document"
"Upload all PDFs from the Reports directory"
"Index the research papers in my Documents folder"
```

**Processing Status:**
```
"Check the status of the Q3 report I uploaded"
"Show me all documents currently being processed"
"Get processing details for document ID abc-123"
```

**List Documents:**
```
"List all my processed documents"
"Show me documents uploaded this week"
"List documents in the financial category"
```

**Delete Documents:**
```
"Delete the old-report document"
"Remove all documents from 2023"
```

### RAG Queries

**Basic Queries:**
```
"What were the main revenue drivers mentioned in the Q3 report?"
"Query my uploaded documents for information about customer retention"
"Search my documents for references to AI regulations"
"Find all mentions of budget constraints in my uploaded files"
```

**Multi-Document Queries:**
```
"Compare the Q2 and Q3 reports and highlight key differences"
"Query all my financial documents about revenue trends over time"
"Search across all research papers for machine learning methodologies"
```

**Queries with Citations:**
```
"What are the key findings in the research papers? Include citations."
"Query the contract for liability clauses with exact page references"
"Summarize the technical specification with source citations"
```

### Advanced Document Operations

**Semantic Search:**
```
"Perform semantic search across all documents for 'customer satisfaction'"
"Find semantically similar content to this paragraph"
"Search for documents with similar themes to the Q3 report"
```

**Hybrid Search:**
```
"Use hybrid search to find documents about 'revenue' and 'growth'"
"Combine keyword and semantic search for 'AI regulations'"
```

**Knowledge Graphs:**
```
"Build a knowledge graph from my uploaded research papers"
"Create an entity graph from the technical documentation"
"Map relationships between concepts in the business strategy docs"
```

**Entity Extraction:**
```
"Extract all entities from the contract document"
"Identify people, organizations, and locations in the reports"
"Use NER to extract key entities from all documents"
```

**Summarization:**
```
"Summarize the quarterly report in 3 bullet points"
"Generate an executive summary of the research paper"
"Create a one-paragraph summary of all uploaded documents"
```

**Table & Image Extraction:**
```
"Extract all tables from the financial statement"
"Get the tables from page 5 of the Q3 report"
"Extract images with OCR from the presentation slides"
```

**Document Comparison:**
```
"Compare the 2023 and 2024 annual reports"
"Highlight differences between version 1 and version 2 of the contract"
"Show me what changed between the two proposals"
```

---

## Desktop & Browser Automation

### Kadis Desktop Automation (7 Tools)

**Mouse Control:**
```
"Move mouse to coordinates 500, 300"
"Click the mouse at current position"
"Right-click at coordinates 800, 400"
"Drag from 100, 100 to 500, 500"
"Double-click at the center of the screen"
```

**Keyboard Control:**
```
"Type 'Hello World' in the active window"
"Press Ctrl+C to copy"
"Press Alt+Tab to switch windows"
"Type my email address: user@example.com"
"Press Enter"
```

**Screenshots:**
```
"Take a screenshot of the entire screen"
"Capture screenshot of region from 0,0 to 1920,1080"
"Take a screenshot and save as screenshot.png"
"Capture the active window"
```

**Window Management:**
```
"List all open windows"
"Show me the window titles"
"Get information about the active window"
```

**Multi-Step Automation:**
```
"Take a screenshot, then move mouse to 500,300 and click"
"Type my password, then press Enter, then take a screenshot"
```

### Playwright Browser Automation

**Navigation:**
```
"Open browser and navigate to github.com"
"Go to the login page at example.com/login"
"Navigate to my GitHub profile"
"Open a new tab and go to google.com"
```

**Interaction:**
```
"Click the login button on the page"
"Fill the email field with test@example.com"
"Click the element with ID 'submit-btn'"
"Select 'Option 2' from the dropdown menu"
```

**Data Extraction:**
```
"Extract all links from the current page"
"Get the text content of the main article"
"Extract all product prices from the page"
"Scrape the table data from the page"
```

**Screenshots:**
```
"Take a screenshot of the current browser page"
"Capture the entire webpage including scrolled content"
"Screenshot the element with class 'pricing-table'"
```

**Wait & Verify:**
```
"Wait for the page to load completely"
"Wait for the element with ID 'content' to appear"
"Verify that the page title is 'Welcome'"
```

### Desktop + Browser Combined

**Multi-Tool Automation:**
```
"Open browser, navigate to the dashboard, take a screenshot,
 then move mouse to the export button and click"

"Navigate to the form, fill it with my data, submit,
 wait for confirmation, then screenshot the result"

"Automate the entire data entry process:
 - Open browser to the form URL
 - Fill each field with data from my clipboard
 - Submit the form
 - Wait for success message
 - Screenshot the confirmation
 - Close browser"
```

---

## Self-Memory System Commands

### Skill Creation (8 Tools)

**Create New Skills:**
```
"Create a skill for analyzing sales reports"
"Make a reusable skill for customer sentiment analysis"
"Create a skill called 'weekly-standup-summary' that summarizes meeting notes"
"Build a skill for extracting financial metrics from documents"
```

**With Full Definition:**
```
"Create a skill called 'code-review-checklist' with the following:
 - Description: Comprehensive code review with security and performance checks
 - Category: development
 - Tags: code, review, security, performance
 - Input: code snippet
 - Output: review checklist with ratings"
```

### Skill Search & Retrieval

**Semantic Search:**
```
"Find skills related to document processing"
"Search my skill library for customer analysis"
"Look for skills about data visualization"
"Find skills in the business_intelligence category"
```

**Filtered Search:**
```
"Show me all skills in the 'development' category"
"List skills tagged with 'analytics' and 'sales'"
"Find skills created this month"
```

### Skill Execution

**Execute by Name:**
```
"Execute the customer-feedback-analysis skill on this data"
"Run the weekly-sales-report skill"
"Use the code-review-checklist skill on this function"
```

**Execute by Search:**
```
"Find and run the skill for analyzing sales data on this report"
"Search for a document processing skill and execute it on Q3_Report.pdf"
```

### Skill Management

**List Skills:**
```
"Show me all my skills"
"List my most used skills"
"Show skills sorted by success rate"
"List skills created this week"
"Show me the top 10 skills by usage count"
```

**Update Skills:**
```
"Update the sales-analysis skill with improved prompt template"
"Modify the customer-sentiment skill description"
"Add the tag 'machine-learning' to the data-analysis skill"
```

**Delete Skills:**
```
"Delete the old-test skill"
"Remove the deprecated-analysis skill"
```

**Skill Statistics:**
```
"Show me statistics for the sales-analysis skill"
"Get usage data for the customer-feedback skill"
"What's the success rate of the code-review skill?"
"How many times has the document-processing skill been used?"
```

**Skill Improvements:**
```
"Suggest improvements for the sales-analysis skill"
"Analyze recent executions of the customer-sentiment skill and recommend updates"
"How can I improve the code-review-checklist skill?"
```

### Self-Learning Workflows

**Automatic Skill Creation:**
```
User performs task repeatedly:
"Analyze this sales report" (3 times this week)

AI Suggests:
"I notice you analyze sales reports frequently. Would you like me to
 create a reusable skill called 'sales-report-analysis'?"

User: "Yes"

System:
→ skill_create with auto-generated definition
→ Stores in Supabase
→ Indexes in Pinecone
→ Available for future use
```

**Skill Evolution:**
```
After 100 uses of a skill:
"The sales-analysis skill has been used 100 times.
 Based on recent executions, I suggest the following improvements:
 - Update prompt template for better accuracy
 - Add new parameter for date range filtering
 - Improve output formatting
 Would you like me to apply these improvements?"
```

---

## Advanced Multi-Tool Workflows

### Multi-Agent + Workflow Automation

**Pattern 1: Agent-Driven Workflow Creation**
```
"Create an automated customer onboarding workflow using FATONI"

Flow:
1. FATONI Strategy Agent → Design onboarding process
2. FATONI Automation Agent → Define automation steps
3. n8n MCP → Generate workflow nodes
4. n8n MCP → Create and activate workflow
5. FATONI Monitoring Agent → Set up monitoring

Command:
"Use FATONI to design a customer onboarding process, then create
 an n8n workflow to automate it, and set up monitoring"
```

**Pattern 2: Document + Code Generation**
```
"Generate code based on the API specification in docs/API.md"

Flow:
1. Filesystem → Read docs/API.md
2. Docling MCP → Process and extract API specs
3. DeepSynaptica → Semantic analysis of requirements
4. FATONI Code Agent → Generate code following specs
5. FATONI Security Agent → Security review
6. Filesystem → Write code files
7. FATONI Code Agent → Generate tests

Command:
"Read the API spec from docs/API.md, analyze requirements with DeepSynaptica,
 generate code with FATONI, perform security review, and write tests"
```

**Pattern 3: Web Scraping + Analysis + Reporting**
```
"Scrape competitor pricing, analyze trends, and create a report"

Flow:
1. FATONI Web Agent → Scrape competitor websites
2. FATONI Analytics Agent → Analyze pricing data
3. DeepSynaptica → Identify trends and patterns
4. FATONI Strategy Agent → Generate strategic insights
5. Filesystem → Write report to markdown
6. Email → Send report to team

Command:
"Use FATONI Web Agent to scrape pricing from competitors.com,
 analyze with Analytics Agent, identify trends with DeepSynaptica,
 generate strategic insights, save report, and email to team@company.com"
```

### Multi-Step Automation Chains

**Pattern 4: Screenshot + Analysis + Action**
```
"Monitor dashboard for errors, screenshot when found, and create GitHub issues"

Flow:
1. Playwright → Navigate to dashboard
2. Playwright → Check for error elements
3. If error found:
   a. Kadis/Playwright → Screenshot
   b. DeepSynaptica → Analyze error context
   c. GitHub MCP → Create issue with screenshot
   d. Slack → Notify team

Command:
"Navigate to dashboard, monitor for errors, screenshot any errors,
 analyze with DeepSynaptica, create GitHub issue with screenshot,
 and notify #engineering on Slack"
```

**Pattern 5: Document Processing + Skill Creation**
```
"Process these research papers and create a skill for future analysis"

Flow:
1. Docling MCP → Upload and process papers
2. DeepSynaptica → Build knowledge graph
3. Skill Memory → Create "research-paper-analysis" skill
   - Prompt template: "Analyze research paper using graph context"
   - Category: research
   - Tags: papers, analysis, academic

Command:
"Upload research papers from Documents/Research/, build knowledge graph,
 and create a reusable skill for analyzing future papers"
```

**Pattern 6: Code Review + Security + Deploy**
```
"Review pull request, run security scan, and deploy if approved"

Flow:
1. GitHub MCP → Get pull request details
2. FATONI Code Agent → Code quality review
3. FATONI Security Agent → Security scan
4. If both pass:
   a. GitHub MCP → Approve PR
   b. GitHub MCP → Merge PR
   c. n8n Workflow → Trigger deployment workflow
   d. FATONI Monitoring Agent → Watch deployment
5. Slack → Notify team of result

Command:
"Review GitHub PR #42, perform security scan, and if approved,
 merge and trigger deployment, then monitor and notify team"
```

---

## Language Support

### German Commands

**Dateioperationen:**
```
"Erstelle eine neue Datei namens config.json im Projektverzeichnis"
"Lade das Dokument report.pdf in den Ordner Downloads hoch"
"Suche in meinen Dokumenten nach Umsatzdaten"
"Liste alle Dateien im Downloads-Ordner auf"
```

**Multi-Agenten:**
```
"Nutze FATONI Code Agent um Python-Code für eine REST-API zu generieren"
"Verwende FATONI Security Agent um diesen Code auf Schwachstellen zu prüfen"
"Delegiere an Auggie: Refaktoriere das Authentifizierungssystem"
"Verwende DeepSynaptica um dieses Dokument semantisch zu analysieren"
```

**Workflow-Automatisierung:**
```
"Erstelle einen n8n-Workflow zur E-Mail-Automatisierung"
"Aktiviere den täglichen Berichts-Workflow"
"Triggere den Kundenintegrations-Workflow für kunde@beispiel.de"
```

**Dokumenten-Intelligence:**
```
"Lade den Quartalsbericht Q3 hoch und analysiere Umsatztrends"
"Suche in meinen hochgeladenen Dokumenten nach Budgetbeschränkungen"
"Erstelle eine Wissensgrafik aus den Forschungspapieren"
```

**Desktop-Automation:**
```
"Mache einen Screenshot vom gesamten Bildschirm"
"Bewege die Maus zu Koordinaten 500, 300 und klicke"
"Tippe 'Hallo Welt' im aktiven Fenster"
```

**Self-Memory:**
```
"Erstelle einen Skill für die Analyse von Verkaufsberichten"
"Suche in meiner Skill-Bibliothek nach Dokumentenverarbeitung"
"Führe den Kundenanalyse-Skill auf diesen Daten aus"
```

### Spanish Commands

**Operaciones de Archivos:**
```
"Crea un nuevo archivo llamado config.json en el directorio del proyecto"
"Sube el documento informe.pdf a la carpeta de Descargas"
"Busca en mis documentos información sobre datos de ventas"
"Lista todos los archivos en la carpeta de Descargas"
```

**Multi-Agentes:**
```
"Usa FATONI Code Agent para generar código Python para una API REST"
"Utiliza FATONI Security Agent para revisar este código en busca de vulnerabilidades"
"Delega a Auggie: Refactoriza el sistema de autenticación"
"Usa DeepSynaptica para analizar semánticamente este documento"
```

**Automatización de Flujos:**
```
"Crea un flujo de trabajo n8n para automatización de correos electrónicos"
"Activa el flujo de trabajo de informes diarios"
"Ejecuta el flujo de integración de clientes para cliente@ejemplo.com"
```

**Inteligencia Documental:**
```
"Sube el informe trimestral Q3 y analiza las tendencias de ingresos"
"Busca en mis documentos subidos restricciones presupuestarias"
"Construye un mapa de conocimiento de los papers de investigación"
```

**Automatización de Escritorio:**
```
"Toma una captura de pantalla de toda la pantalla"
"Mueve el ratón a las coordenadas 500, 300 y haz clic"
"Escribe 'Hola Mundo' en la ventana activa"
```

**Auto-Memoria:**
```
"Crea una habilidad para analizar informes de ventas"
"Busca en mi biblioteca de habilidades procesamiento de documentos"
"Ejecuta la habilidad de análisis de clientes en estos datos"
```

---

## Best Practices

### Command Design

**✅ Do:**
- Be explicit about agents when you have a preference
- Specify file paths completely (absolute or clear relative)
- Include all necessary parameters upfront
- Use natural language (AI understands context)
- Chain related operations in one command when logical
- Specify output format when needed (JSON, markdown, etc.)

**❌ Avoid:**
- Overly complex nested commands (break into steps)
- Ambiguous references ("that file", "the document")
- Missing critical details (which document? which agent?)
- Commands that require clarification (ask yourself first)

### Multi-Agent Efficiency

**Sequential vs Parallel:**
```
✅ Parallel (when tasks are independent):
"Use FATONI Code Agent to generate code AND
 FATONI Analytics Agent to analyze data simultaneously"

✅ Sequential (when tasks depend on each other):
"Use FATONI Code Agent to generate code, THEN
 FATONI Security Agent to review it, THEN
 FATONI Code Agent to fix issues"
```

### Error Recovery

**Graceful Degradation:**
```
User: "Upload Q3_Report.pdf and query for revenue data"

If upload fails:
AI: "The upload failed due to network error. Would you like me to:
     a) Retry the upload
     b) Try with a different file
     c) Cancel and show error details"

User: "Retry"
AI: → Retries upload → Continues with query
```

**Clarification Prompts:**
```
User: "Analyze the report"

AI: "I found 3 reports: Q3_Financial, Q4_Sales, Annual_Summary.
     Which would you like me to analyze?"

User: "Q3_Financial"

AI: "Which agent should I use?
     a) FATONI Analytics (data analysis)
     b) DeepSynaptica (semantic analysis)
     c) Both"

User: "FATONI Analytics"
```

### Performance Optimization

**Batching:**
```
Instead of:
"Upload document1.pdf"
"Upload document2.pdf"
"Upload document3.pdf"

Say:
"Upload all PDFs from the Reports folder"
→ Single batch operation, faster
```

**Caching:**
```
For repeated queries on same document:
First time: "Upload Q3_Report.pdf and query for revenue data"
→ Document processed, embedded, cached

Subsequent: "Query the Q3 report about expenses"
→ Uses cached embeddings, much faster
```

**Lazy Execution:**
```
Defer expensive operations until needed:
"Create a workflow but don't activate it yet"
"Generate code but don't execute tests until I review"
```

### Security Best Practices

**Sensitive Data:**
```
✅ Do:
"Upload document.pdf but redact social security numbers"
"Scan code for vulnerabilities but don't log the code itself"

❌ Avoid:
Voice commands containing passwords, API keys, or PII
```

**Confirmations:**
```
For destructive actions, system should confirm:

User: "Delete all old documents"
AI: "⚠️ This will delete 47 documents. Are you sure? (yes/no)"
User: "Yes"
AI: → Proceeds
```

---

## Voice-Specific Considerations

### Pronunciation

**Clear Articulation:**
```
Filenames:
"config dot j-s-o-n" (config.json)
"app dot p-y" (app.py)
"README dot m-d" (README.md)

Paths:
"slash Users slash username slash Documents"
"/Users/username/Documents"

Special Characters:
"underscore" for _
"dash" or "hyphen" for -
"period" or "dot" for .
"slash" for /
"at" for @
```

**Spelling Out Ambiguous Terms:**
```
"Create a file called A-P-I underscore config dot json"
→ API_config.json

"Navigate to H-T-T-P-S colon slash slash github dot com"
→ https://github.com
```

### Natural Speech Patterns

```
✅ Natural (works well):
"Hey, can you upload the Q3 report to DeepALL and tell me about revenue trends?"
"I need you to use FATONI Code Agent to generate a REST API in Python"
"Please create an n8n workflow for email automation"

✅ Direct (also works):
"Upload Q3_Report.pdf to DeepALL and query for revenue trends"
"FATONI Code Agent: Generate Python REST API"
"n8n: Create email automation workflow"
```

### Handling Corrections

```
User: "Upload the report from last week"
AI: "I found 3 reports from last week. Which one?"
User: "The sales report"
AI: "Got it, uploading Q3_Sales_Report.pdf..."

Or:

User: "Upload the... actually, first check if it exists"
AI: "Checking for the file first..."
```

---

## Testing Your Commands

### Iterative Refinement

```
Start Simple → Add Detail → Optimize

Level 1: "Analyze document"
→ Too vague

Level 2: "Analyze Q3_Report.pdf"
→ Better, but which type of analysis?

Level 3: "Use FATONI Analytics to analyze sales trends in Q3_Report.pdf"
→ Clear and actionable ✅

Level 4: "Use FATONI Analytics Agent to analyze year-over-year sales trends
          in Q3_Report.pdf and create a visualization"
→ Optimal specificity ✅
```

### Command Validation

**Before Executing, Check:**
1. Is the agent/tool specified or obvious from context?
2. Are all required parameters included?
3. Is the file/document path clear and correct?
4. Is the desired output format specified if needed?
5. Are there any destructive actions that need confirmation?

### Success Criteria

**A good voice command:**
- ✅ Can be executed without clarification
- ✅ Produces expected results on first try
- ✅ Is reproducible (same command → same result)
- ✅ Is concise but complete
- ✅ Uses natural language

---

## Examples by Complexity

### Simple (Single Tool, Single Agent)

```
"List my GitHub notifications"
→ GitHub MCP: list_notifications

"Read config.json"
→ Filesystem MCP: read_file

"Use FATONI Code Agent to generate a Fibonacci function"
→ FATONI Code Agent: fatoni_code_generate
```

### Medium (Multiple Tools, Single Agent)

```
"Upload Q3_Report.pdf and query for revenue trends"
→ Docling MCP: upload_document
→ Docling MCP: query_documents

"Use FATONI to generate code and then review it"
→ FATONI Code Agent: fatoni_code_generate
→ FATONI Code Agent: fatoni_code_review

"Create an n8n workflow and activate it"
→ n8n MCP: n8n_create_workflow
→ n8n MCP: n8n_activate_workflow
```

### Complex (Multiple Tools, Multiple Agents)

```
"Build a secure login system with analytics"
→ FATONI Code Agent: Generate auth code
→ FATONI Security Agent: Security review
→ FATONI Analytics Agent: Add analytics tracking
→ FATONI Code Agent: Generate tests
→ Filesystem MCP: Write files

"Scrape competitor pricing, analyze trends, and create n8n workflow for monitoring"
→ FATONI Web Agent: Scrape websites
→ FATONI Analytics Agent: Analyze pricing data
→ DeepSynaptica: Identify patterns
→ n8n MCP: Create monitoring workflow
→ n8n MCP: Activate workflow

"Process research papers, build knowledge graph, and create reusable skill"
→ Docling MCP: Upload documents
→ Docling MCP: Process documents
→ DeepSynaptica: Build knowledge graph
→ Skill Memory: Create skill
→ Pinecone: Index skill embeddings
```

### Expert (Full Ecosystem, Orchestrated)

```
"Implement a new feature end-to-end with full automation"

Flow:
1. GitHub MCP → Create feature branch
2. FATONI Strategy Agent → Define feature requirements
3. FATONI Code Agent → Generate code
4. FATONI Designer Agent → Create UI components
5. FATONI Security Agent → Security review
6. FATONI Code Agent → Generate tests
7. Filesystem MCP → Write all files
8. GitHub MCP → Commit changes
9. GitHub MCP → Create pull request
10. n8n MCP → Create workflow to monitor PR
11. Slack → Notify team

Command:
"Create a complete user authentication feature:
 - Generate requirements with Strategy Agent
 - Generate code with Code Agent
 - Design UI with Designer Agent
 - Security review with Security Agent
 - Write tests
 - Commit to GitHub
 - Create PR
 - Set up monitoring workflow
 - Notify team on Slack"
```

---

## Summary: Command Design Checklist

Before issuing a voice command, ask yourself:

1. ✅ **What** do I want to accomplish? (Be specific)
2. ✅ **Which** agent/tool should do it? (Specify or let AI choose)
3. ✅ **Where** is the data/file? (Provide full path or clear reference)
4. ✅ **How** should the output look? (Specify format if needed)
5. ✅ **When** should it execute? (Now, scheduled, triggered?)
6. ✅ **Why** am I doing this? (Context helps AI make better decisions)

**Golden Rule:**
> Speak naturally, but be specific. AI understands context, but precision reduces errors.

---

**Remember**: DeepAllSpeak with 20+ MCP servers and 16 AI agents gives you incredible power. Use clear, specific commands to harness it effectively!
