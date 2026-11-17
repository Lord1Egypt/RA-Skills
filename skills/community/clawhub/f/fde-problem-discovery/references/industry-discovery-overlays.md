# Industry Discovery Overlay

## Usage principles

First use the common problem discovery process to restore the real tasks, and then add evidence and constraint problems according to industries. Industry overlays cannot replace customer on-site evidence, nor can they translate public industry patterns directly into current customer facts.

## Financial Services

### Prioritize understanding

- Which tasks are recommendations, approvals, transactions, records or regulatory reports;
- Who has the final decision-making power, and which actions must be reviewed by two people;
- System record sources for customers, accounts, transactions and model outputs;
- Appropriateness, explainability, auditing, data geography and record retention requirements;
- What are the losses caused by wrong rejection, wrong approval, delay and manual review.

### Evidence

- Masked cases, rule hits, review records, appeals, exceptions and audit trails;
- Baselines stratified by customer type, product, risk level and channel;
- Conflicting perspectives of compliance, legal, model risk, information security and frontline users.

### Cannot default

- Historical artificial decisions are naturally correct;
- High accuracy can offset a small number of costly errors;
- Interpreting the text is equivalent to satisfying regulatory interpretation obligations;
- POC de-identified data represents production data distribution.

## Healthcare and Life Sciences

### Prioritize understanding

- Is the current task administrative, operational, research support, or clinical decision-making;
- Who is responsible for the results and whether the error affected diagnosis and treatment, patient safety or informed consent;
- Data minimization, authorization, de-identification, geography and retention boundaries;
- Workflow differences for clinical, coding, operational and patient users;
- Which scenarios must be judged by qualified professionals.

### Evidence

- De-identify task samples, review disagreements, wait times, rework, escalations and security incidents;
- Representativeness of different populations, departments, facilities or institutions;
- Clinical safety, privacy, ethics, legal affairs and information security review opinions.

### Cannot default

- Disclosure of medical knowledge can serve as a substitute for institutional policy and patient context;
- A small sample of expert reviews can be extrapolated to all users;
- POC is a medical device, clinical recommendation, or manufacturing use approval.

## Manufacturing and Supply Chain

### Prioritize understanding

- Whether the task occurs in planning, quality, maintenance, warehousing or field control;
- How IT, OT, devices, sensors and human records flow between each other;
- Network outages, shifts, noise, equipment differences and site safety constraints;
- The relative costs of downtime, scrap, delays, missed inspections and false downtime;
- How the front line continues to work and recover when systems fail.

### Evidence

- Event timeline, equipment logs, maintenance orders, quality records, shift observations and material tracking;
- Normal, abnormal, seasonal and extreme load samples;
- Field Operator, Process, Quality, Equipment,IT/OTSafety and Manager Perspectives.

### Cannot default

- Continuous networking in the cloud;
- Equipment of the same model has the same configuration;
- Simulation or historical replay equals on-site safety verification;
- Reducing manual actions will definitely reduce risks.

## Enterprise Customer Service and Operations

### Prioritize understanding

- Differences between formal processes and actual frontline processes;
- System switching between ticket, CRM, knowledge base, chat and forms;
- Normal path, exceptions, special contracts, complaints and upgrades;
- Trade-offs between quality, processing time, rework, customer experience and compliance;
- Whether the new scheme adds review, login, copy-paste or interpretation burden.

### Evidence

- Recent real ticket, processing tracks, content before and after modifications, knowledge references and upgrade records;
- Baseline stratified by type, complexity, channel, customer level and personnel experience;
- Usage, disapproval and bypass behavior, not just satisfaction.

### Cannot default

- The "auto-reply" is the correct question;
- A decrease in average processing time represents overall value;
- Management hopes that promotion will lead to adoption by frontline professionals;
- Knowledge base content is always up-to-date, conflict-free and available to all customers.

## Public transportation and travel operations

### Prioritize understanding

- The tasks occur in driving organization, passenger transport services, equipment maintenance, incident analysis and judgment, or external information release;
- Who is responsible for assessment, who has scheduling rights, who has security authorization, and whether the agent may cross any of these layers;
- The respective system sources, update times and authority levels of vehicle locations, shifts, routes, road announcements, on-site reports and emergency plans;
- How the workflow changes during normal delays, road closures, vehicle breakdowns, extreme weather, heavy passenger flow, and communication disruptions;
- What are the impacts of missing real risks, false positive events, using expired notifications, incorrect scheduling and delayed processing;
- Whether the information obtained by frontline employees, dispatchers, safety managers, customer service and passengers is consistent, and who will arbitrate in the event of conflicts.

### Evidence

- Timeline of de-identification events, vehicle location snapshots, driving plans, road or weather notices, driver reports, dispatch logs and review records;
- The generation time, collection time, validity period, delay and missing rate of each dynamic data, not just whether the field exists;
- Processing time and results stratified by event type, line, time period, weather, severity and communication status;
- Intersecting perspectives from dispatch, safety, fleet, depot, customer service, information dissemination and frontline drivers;
- Records of manual takeover, downgraded operation, notification and approval, false alarms, missed alarms and danger escalation.

### Security boundaries that must be established separately

- assessment assistance, plan drafting, dispatching instructions, vehicle control, and external release are five different permissions and cannot be written as one "automatic processing" capability;
- Dynamic evidence must have a timestamp and validity status; if it is expired, from unknown sources or conflicting with each other, the conclusion should be blocked and manual confirmation requested;
- POC gives priority to historical playback, shadow mode or read-only environment, and does not directly change vehicles, signals, routes or passenger information in transit;
- Any recommendations must show the basis, missing information, uncertainty and ultimate responsibility; safety rules cannot be covered by natural language samples;
- Traffic regulations, corporate emergency plans, local competent department rules and on-site command relationships need to be confirmed by customers one by one. Public information can only be used to raise questions.

### Cannot default

- Vehicle location, road announcements or field reports are real-time and consistent with each other;
- Historical processing results are naturally correct, or can represent extreme weather and major events;
- Shortening assessment time equals improved safety results;
- Obtain production scheduling authorization through simulation, offline playback or shadow mode;
- If the dispatcher adopts the suggestion, it proves that the suggestion is correct, or if he fails to adopt it, it proves that the suggestion is worthless;
- The disposal script of a city, line or operating entity can be copied to another site as it is.

## Output requirements

When adding "industry overlay conclusions" to the discovery package, mark them one by one: disclosure of industry assumptions, customer evidence, counter-evidence, risk manager and next steps to supplement evidence. Industry models without customer evidence can only be interview questions, not requirements.
