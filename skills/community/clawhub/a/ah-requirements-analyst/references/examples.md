# Requirements Analyst — Code Examples

## Example 1

```typescript
// requirements-analyzer.ts
import { v4 as uuidv4 } from 'uuid';
import { EventEmitter } from 'events';

interface Requirement {
  id: string;
  title: string;
  description: string;
  type: RequirementType;
  priority: Priority;
  category: string;
  source: StakeholderInfo;
  status: RequirementStatus;
  acceptanceCriteria: AcceptanceCriterion[];
  dependencies: string[];
  constraints: Constraint[];
  assumptions: string[];
  risks: Risk[];
  traceability: Traceability;
  validation: ValidationInfo;
  createdAt: Date;
  updatedAt: Date;
  version: number;
}

interface UserStory {
  id: string;
  title: string;
  asA: string;
  iWant: string;
  soThat: string;
  acceptanceCriteria: AcceptanceCriterion[];
  priority: Priority;
  storyPoints?: number;
  epic?: string;
  sprint?: string;
  dependencies: string[];
  tasks: Task[];
  testCases: TestCase[];
  notes: string;
  status: StoryStatus;
}

interface AcceptanceCriterion {
  id: string;
  given: string;
  when: string;
  then: string;
  verified: boolean;
  testCaseIds: string[];
}

class RequirementsAnalyzer extends EventEmitter {
  private requirements: Map<string, Requirement> = new Map();
  private userStories: Map<string, UserStory> = new Map();
  private stakeholders: Map<string, Stakeholder> = new Map();
  private traceabilityMatrix: TraceabilityMatrix;
  private validationRules: ValidationRule[] = [];

  constructor() {
    super();
    this.traceabilityMatrix = new TraceabilityMatrix();
    this.initializeValidationRules();
  }

  async analyzeRequirements(input: RequirementInput): Promise<RequirementAnalysis> {
    // Parse and categorize requirements
    const parsed = await this.parseRequirements(input);
    
    // Identify stakeholders
    const stakeholders = await this.identifyStakeholders(parsed);
    
    // Analyze completeness
    const completeness = this.analyzeCompleteness(parsed);
    
    // Check consistency
    const consistency = this.checkConsistency(parsed);
    
    // Identify conflicts
    const conflicts = this.identifyConflicts(parsed);
    
    // Analyze feasibility
    const feasibility = await this.analyzeFeasibility(parsed);
    
    // Generate recommendations
    const recommendations = this.generateRecommendations({
      parsed,
      completeness,
      consistency,
      conflicts,
      feasibility,
    });
    
    // Create traceability matrix
    this.buildTraceabilityMatrix(parsed);
    
    return {
      requirements: parsed,
      stakeholders,
      completeness,
      consistency,
      conflicts,
      feasibility,
      recommendations,
      traceabilityMatrix: this.traceabilityMatrix.export(),
    };
  }

  async createUserStory(input: UserStoryInput): Promise<UserStory> {
    const story: UserStory = {
      id: this.generateId('US'),
      title: input.title,
      asA: input.asA,
      iWant: input.iWant,
      soThat: input.soThat,
      acceptanceCriteria: this.generateAcceptanceCriteria(input),
      priority: input.priority || Priority.MEDIUM,
      storyPoints: input.storyPoints,
      epic: input.epic,
      sprint: input.sprint,
      dependencies: input.dependencies || [],
      tasks: this.generateTasks(input),
      testCases: this.generateTestCases(input),
      notes: input.notes || '',
      status: StoryStatus.DRAFT,
    };
    
    // Validate user story
    this.validateUserStory(story);
    
    // Check for duplicates
    this.checkDuplicateStories(story);
    
    // Store user story
    this.userStories.set(story.id, story);
    
    // Update traceability
    this.updateTraceability(story);
    
    this.emit('userStory:created', story);
    
    return story;
  }

  private generateAcceptanceCriteria(input: UserStoryInput): AcceptanceCriterion[] {
    const criteria: AcceptanceCriterion[] = [];
    
    if (input.acceptanceCriteria) {
      for (const ac of input.acceptanceCriteria) {
        criteria.push({
          id: this.generateId('AC'),
          given: ac.given,
          when: ac.when,
          then: ac.then,
          verified: false,
          testCaseIds: [],
        });
      }
    } else {
      // Generate default acceptance criteria based on story
      criteria.push({
        id: this.generateId('AC'),
        given: `User is ${input.asA}`,
        when: `User ${input.iWant}`,
        then: `System ${input.soThat}`,
        verified: false,
        testCaseIds: [],
      });
    }
    
    return criteria;
  }

  private generateTasks(input: UserStoryInput): Task[] {
    const tasks: Task[] = [];
    
    // Frontend tasks
    if (this.requiresFrontend(input)) {
      tasks.push({
        id: this.generateId('TASK'),
        title: 'Implement UI components',
        description: 'Create necessary UI components for the feature',
        type: TaskType.DEVELOPMENT,
        estimatedHours: 8,
        assignee: null,
        status: TaskStatus.TODO,
      });
    }
    
    // Backend tasks
    if (this.requiresBackend(input)) {
      tasks.push({
        id: this.generateId('TASK'),
        title: 'Implement API endpoints',
        description: 'Create backend API endpoints',
        type: TaskType.DEVELOPMENT,
        estimatedHours: 6,
        assignee: null,
        status: TaskStatus.TODO,
      });
      
      tasks.push({
        id: this.generateId('TASK'),
        title: 'Database schema updates',
        description: 'Update database schema if needed',
        type: TaskType.DEVELOPMENT,
        estimatedHours: 2,
        assignee: null,
        status: TaskStatus.TODO,
      });
    }
    
    // Testing tasks
    tasks.push({
      id: this.generateId('TASK'),
      title: 'Write unit tests',
      description: 'Create unit tests for new functionality',
      type: TaskType.TESTING,
      estimatedHours: 4,
      assignee: null,
      status: TaskStatus.TODO,
    });
    
    tasks.push({
      id: this.generateId('TASK'),
      title: 'Integration testing',
      description: 'Perform integration testing',
      type: TaskType.TESTING,
      estimatedHours: 3,
      assignee: null,
      status: TaskStatus.TODO,
    });
    
    // Documentation
    tasks.push({
      id: this.generateId('TASK'),
      title: 'Update documentation',
      description: 'Update user and technical documentation',
      type: TaskType.DOCUMENTATION,
      estimatedHours: 2,
      assignee: null,
      status: TaskStatus.TODO,
    });
    
    return tasks;
  }

  private generateTestCases(input: UserStoryInput): TestCase[] {
    const testCases: TestCase[] = [];
    
    // Generate test cases for each acceptance criterion
    for (const ac of input.acceptanceCriteria || []) {
      // Happy path test
      testCases.push({
        id: this.generateId('TC'),
        title: `Verify ${ac.then}`,
        description: `Test that ${ac.then} when ${ac.when}`,
        type: TestType.FUNCTIONAL,
        priority: Priority.HIGH,
        preconditions: [ac.given],
        steps: [
          { action: ac.when, expectedResult: ac.then },
        ],
        expectedResult: ac.then,
        status: TestStatus.NOT_EXECUTED,
      });
      
      // Edge case test
      testCases.push({
        id: this.generateId('TC'),
        title: `Edge case for ${ac.then}`,
        description: `Test edge cases for ${ac.then}`,
        type: TestType.EDGE_CASE,
        priority: Priority.MEDIUM,
        preconditions: [ac.given],
        steps: [
          { action: `Invalid ${ac.when}`, expectedResult: 'Appropriate error handling' },
        ],
        expectedResult: 'System handles edge case gracefully',
        status: TestStatus.NOT_EXECUTED,
      });
    }
    
    // Performance test
    if (this.requiresPerformanceTest(input)) {
      testCases.push({
        id: this.generateId('TC'),
        title: 'Performance test',
        description: 'Verify performance requirements',
        type: TestType.PERFORMANCE,
        priority: Priority.MEDIUM,
        preconditions: ['System under normal load'],
        steps: [
          { action: 'Execute feature', expectedResult: 'Response time < 1s' },
        ],
        expectedResult: 'Meets performance criteria',
        status: TestStatus.NOT_EXECUTED,
      });
    }
    
    // Security test
    if (this.requiresSecurityTest(input)) {
      testCases.push({
        id: this.generateId('TC'),
        title: 'Security validation',
        description: 'Verify security requirements',
        type: TestType.SECURITY,
        priority: Priority.HIGH,
        preconditions: ['User authenticated'],
        steps: [
          { action: 'Attempt unauthorized access', expectedResult: 'Access denied' },
        ],
        expectedResult: 'Security measures effective',
        status: TestStatus.NOT_EXECUTED,
      });
    }
    
    return testCases;
  }

  async elicitRequirements(stakeholders: Stakeholder[]): Promise<Requirement[]> {
    const requirements: Requirement[] = [];
    
    for (const stakeholder of stakeholders) {
      // Conduct interview
      const interviewResults = await this.conductInterview(stakeholder);
      
      // Analyze responses
      const analyzed = this.analyzeInterviewResponses(interviewResults);
      
      // Extract requirements
      const extracted = this.extractRequirements(analyzed, stakeholder);
      
      requirements.push(...extracted);
    }
    
    // Remove duplicates
    const unique = this.removeDuplicateRequirements(requirements);
    
    // Prioritize requirements
    const prioritized = this.prioritizeRequirements(unique, stakeholders);
    
    return prioritized;
  }

  private async conductInterview(stakeholder: Stakeholder): Promise<InterviewResult> {
    const questions = this.generateInterviewQuestions(stakeholder);
    
    // Simulate interview process
    const responses: InterviewResponse[] = [];
    
    for (const question of questions) {
      responses.push({
        question,
        answer: await this.getStakeholderResponse(stakeholder, question),
        followUps: this.generateFollowUpQuestions(question),
      });
    }
    
    return {
      stakeholder,
      date: new Date(),
      responses,
      insights: this.extractInsights(responses),
      actionItems: this.identifyActionItems(responses),
    };
  }

  private generateInterviewQuestions(stakeholder: Stakeholder): Question[] {
    const questions: Question[] = [];
    
    // Context questions
    questions.push({
      id: this.generateId('Q'),
      text: 'Can you describe your role and how you interact with the system?',
      type: QuestionType.OPEN_ENDED,
      category: 'context',
    });
    
    // Problem identification
    questions.push({
      id: this.generateId('Q'),
      text: 'What are the main challenges you face with the current system?',
      type: QuestionType.OPEN_ENDED,
      category: 'problem',
    });
    
    // Goals and objectives
    questions.push({
      id: this.generateId('Q'),
      text: 'What would you like to achieve with the new system?',
      type: QuestionType.OPEN_ENDED,
      category: 'goal',
    });
    
    // Functional requirements
    questions.push({
      id: this.generateId('Q'),
      text: 'What specific features or functionalities do you need?',
      type: QuestionType.OPEN_ENDED,
      category: 'functional',
    });
    
    // Non-functional requirements
    questions.push({
      id: this.generateId('Q'),
      text: 'What are your expectations regarding performance, security, and usability?',
      type: QuestionType.OPEN_ENDED,
      category: 'non-functional',
    });
    
    // Constraints
    questions.push({
      id: this.generateId('Q'),
      text: 'Are there any constraints or limitations we should be aware of?',
      type: QuestionType.OPEN_ENDED,
      category: 'constraint',
    });
    
    // Success criteria
    questions.push({
      id: this.generateId('Q'),
      text: 'How would you measure the success of this project?',
      type: QuestionType.OPEN_ENDED,
      category: 'success',
    });
    
    return questions;
  }

  private analyzeCompleteness(requirements: Requirement[]): CompletenessAnalysis {
    const analysis: CompletenessAnalysis = {
      score: 0,
      missingElements: [],
      recommendations: [],
    };
    
    // Check for required elements
    const requiredElements = [
      'functional_requirements',
      'non_functional_requirements',
      'acceptance_criteria',
      'constraints',
      'assumptions',
      'dependencies',
    ];
    
    const foundElements = new Set<string>();
    
    for (const req of requirements) {
      if (req.type === RequirementType.FUNCTIONAL) {
        foundElements.add('functional_requirements');
      }
      if (req.type === RequirementType.NON_FUNCTIONAL) {
        foundElements.add('non_functional_requirements');
      }
      if (req.acceptanceCriteria.length > 0) {
        foundElements.add('acceptance_criteria');
      }
      if (req.constraints.length > 0) {
        foundElements.add('constraints');
      }
      if (req.assumptions.length > 0) {
        foundElements.add('assumptions');
      }
      if (req.dependencies.length > 0) {
        foundElements.add('dependencies');
      }
    }
    
    // Calculate completeness score
    analysis.score = (foundElements.size / requiredElements.length) * 100;
    
    // Identify missing elements
    for (const element of requiredElements) {
      if (!foundElements.has(element)) {
        analysis.missingElements.push(element);
        analysis.recommendations.push(`Add ${element.replace('_', ' ')}`);
      }
    }
    
    // Check individual requirement completeness
    for (const req of requirements) {
      const reqCompleteness = this.checkRequirementCompleteness(req);
      if (reqCompleteness < 80) {
        analysis.recommendations.push(
          `Requirement ${req.id} is only ${reqCompleteness}% complete`
        );
      }
    }
    
    return analysis;
  }

  private checkRequirementCompleteness(req: Requirement): number {
    let score = 0;
    const weights = {
      description: 20,
      acceptanceCriteria: 30,
      priority: 10,
      source: 10,
      constraints: 10,
      assumptions: 10,
      risks: 10,
    };
    
    if (req.description && req.description.length > 50) score += weights.description;
    if (req.acceptanceCriteria.length > 0) score += weights.acceptanceCriteria;
    if (req.priority) score += weights.priority;
    if (req.source) score += weights.source;
    if (req.constraints.length > 0) score += weights.constraints;
    if (req.assumptions.length > 0) score += weights.assumptions;
    if (req.risks.length > 0) score += weights.risks;
    
    return score;
  }

  private checkConsistency(requirements: Requirement[]): ConsistencyAnalysis {
    const issues: ConsistencyIssue[] = [];
    
    // Check for conflicting requirements
    for (let i = 0; i < requirements.length; i++) {
      for (let j = i + 1; j < requirements.length; j++) {
        const conflict = this.detectConflict(requirements[i], requirements[j]);
        if (conflict) {
          issues.push({
            type: 'conflict',
            requirementIds: [requirements[i].id, requirements[j].id],
            description: conflict,
            severity: Severity.HIGH,
          });
        }
      }
    }
    
    // Check for ambiguous language
    for (const req of requirements) {
      const ambiguities = this.detectAmbiguities(req);
      for (const ambiguity of ambiguities) {
        issues.push({
          type: 'ambiguity',
          requirementIds: [req.id],
          description: ambiguity,
          severity: Severity.MEDIUM,
        });
      }
    }
    
    // Check for incomplete references
    for (const req of requirements) {
      for (const dep of req.dependencies) {
        if (!requirements.find(r => r.id === dep)) {
          issues.push({
            type: 'missing_dependency',
            requirementIds: [req.id],
            description: `Missing dependency: ${dep}`,
            severity: Severity.HIGH,
          });
        }
      }
    }
    
    return {
      isConsistent: issues.length === 0,
      issues,
      score: Math.max(0, 100 - (issues.length * 10)),
    };
  }

  private detectConflict(req1: Requirement, req2: Requirement): string | null {
    // Check for direct contradictions
    const keywords1 = this.extractKeywords(req1.description);
    const keywords2 = this.extractKeywords(req2.description);
    
    // Simple conflict detection logic
    if (keywords1.includes('must') && keywords2.includes('must not')) {
      const common = keywords1.filter(k => keywords2.includes(k));
      if (common.length > 0) {
        return `Conflicting requirements about: ${common.join(', ')}`;
      }
    }
    
    return null;
  }

  private detectAmbiguities(req: Requirement): string[] {
    const ambiguities: string[] = [];
    const ambiguousWords = [
      'appropriate',
      'adequate',
      'as needed',
      'as required',
      'easy',
      'efficient',
      'fast',
      'flexible',
      'improved',
      'maximized',
      'minimized',
      'optimized',
      'quick',
      'robust',
      'seamless',
      'simple',
      'sufficient',
      'suitable',
      'user-friendly',
      'various',
    ];
    
    const description = req.description.toLowerCase();
    for (const word of ambiguousWords) {
      if (description.includes(word)) {
        ambiguities.push(`Ambiguous term "${word}" needs clarification`);
      }
    }
    
    return ambiguities;
  }

  private buildTraceabilityMatrix(requirements: Requirement[]): void {
    for (const req of requirements) {
      // Link to source
      if (req.source) {
        this.traceabilityMatrix.addLink(
          req.id,
          req.source.id,
          LinkType.DERIVED_FROM
        );
      }
      
      // Link to dependencies
      for (const dep of req.dependencies) {
        this.traceabilityMatrix.addLink(
          req.id,
          dep,
          LinkType.DEPENDS_ON
        );
      }
      
      // Link to test cases
      for (const ac of req.acceptanceCriteria) {
        for (const tcId of ac.testCaseIds) {
          this.traceabilityMatrix.addLink(
            req.id,
            tcId,
            LinkType.VERIFIED_BY
          );
        }
      }
    }
  }

  private validateUserStory(story: UserStory): void {
    const errors: string[] = [];
    
    // Check INVEST criteria
    if (!this.isIndependent(story)) {
      errors.push('Story is not independent');
    }
    
    if (!this.isNegotiable(story)) {
      errors.push('Story is too prescriptive');
    }
    
    if (!this.isValuable(story)) {
      errors.push('Story does not clearly provide value');
    }
    
    if (!this.isEstimable(story)) {
      errors.push('Story is too vague to estimate');
    }
    
    if (!this.isSmall(story)) {
      errors.push('Story is too large');
    }
    
    if (!this.isTestable(story)) {
      errors.push('Story lacks testable acceptance criteria');
    }
    
    if (errors.length > 0) {
      console.warn(`User story ${story.id} validation issues:`, errors);
    }
  }

  private isIndependent(story: UserStory): boolean {
    return story.dependencies.length === 0 || story.dependencies.length <= 2;
  }

  private isNegotiable(story: UserStory): boolean {
    // Check if story is not overly detailed
    return story.acceptanceCriteria.length <= 10;
  }

  private isValuable(story: UserStory): boolean {
    // Check if "so that" clause provides clear value
    return story.soThat && story.soThat.length > 10;
  }

  private isEstimable(story: UserStory): boolean {
    // Check if story has enough detail to estimate
    return story.acceptanceCriteria.length > 0;
  }

  private isSmall(story: UserStory): boolean {
    // Check if story points are reasonable
    return !story.storyPoints || story.storyPoints <= 13;
  }

  private isTestable(story: UserStory): boolean {
    // Check if acceptance criteria are testable
    return story.acceptanceCriteria.every(ac => 
      ac.given && ac.when && ac.then
    );
  }

  private generateId(prefix: string): string {
    return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private extractKeywords(text: string): string[] {
    // Simple keyword extraction
    const words = text.toLowerCase().split(/\s+/);
    const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at']);
    return words.filter(w => !stopWords.has(w) && w.length > 3);
  }

  private requiresFrontend(input: UserStoryInput): boolean {
    const uiKeywords = ['interface', 'screen', 'page', 'form', 'button', 'display'];
    const text = `${input.iWant} ${input.soThat}`.toLowerCase();
    return uiKeywords.some(k => text.includes(k));
  }

  private requiresBackend(input: UserStoryInput): boolean {
    const backendKeywords = ['api', 'database', 'store', 'retrieve', 'process', 'calculate'];
    const text = `${input.iWant} ${input.soThat}`.toLowerCase();
    return backendKeywords.some(k => text.includes(k));
  }

  private requiresPerformanceTest(input: UserStoryInput): boolean {
    const perfKeywords = ['fast', 'quick', 'performance', 'speed', 'responsive'];
    const text = `${input.iWant} ${input.soThat}`.toLowerCase();
    return perfKeywords.some(k => text.includes(k));
  }

  private requiresSecurityTest(input: UserStoryInput): boolean {
    const securityKeywords = ['secure', 'authenticate', 'authorize', 'permission', 'access'];
    const text = `${input.iWant} ${input.soThat}`.toLowerCase();
    return securityKeywords.some(k => text.includes(k));
  }

  private initializeValidationRules(): void {
    this.validationRules = [
      {
        id: 'REQ-VAL-001',
        name: 'Description Length',
        check: (req: Requirement) => req.description.length >= 50,
        message: 'Requirement description should be at least 50 characters',
      },
      {
        id: 'REQ-VAL-002',
        name: 'Acceptance Criteria',
        check: (req: Requirement) => req.acceptanceCriteria.length > 0,
        message: 'Requirement must have at least one acceptance criterion',
      },
      {
        id: 'REQ-VAL-003',
        name: 'Priority Set',
        check: (req: Requirement) => req.priority !== undefined,
        message: 'Requirement must have a priority',
      },
    ];
  }
}

// Supporting classes
class TraceabilityMatrix {
  private links: Map<string, Set<TraceLink>> = new Map();

  addLink(from: string, to: string, type: LinkType): void {
    if (!this.links.has(from)) {
      this.links.set(from, new Set());
    }
    
    this.links.get(from)!.add({
      from,
      to,
      type,
      created: new Date(),
    });
  }

  getLinks(id: string): TraceLink[] {
    return Array.from(this.links.get(id) || []);
  }

  export(): any {
    const matrix: any = {};
    
    for (const [from, links] of this.links) {
      matrix[from] = Array.from(links).map(link => ({
        to: link.to,
        type: link.type,
      }));
    }
    
    return matrix;
  }
}

// Type definitions
enum RequirementType {
  FUNCTIONAL = 'functional',
  NON_FUNCTIONAL = 'non_functional',
  CONSTRAINT = 'constraint',
  BUSINESS = 'business',
  TECHNICAL = 'technical',
}

enum Priority {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

enum RequirementStatus {
  DRAFT = 'draft',
  REVIEW = 'review',
  APPROVED = 'approved',
  IMPLEMENTED = 'implemented',
  VERIFIED = 'verified',
}

enum StoryStatus {
  DRAFT = 'draft',
  READY = 'ready',
  IN_PROGRESS = 'in_progress',
  TESTING = 'testing',
  DONE = 'done',
}

enum TaskType {
  DEVELOPMENT = 'development',
  TESTING = 'testing',
  DOCUMENTATION = 'documentation',
  REVIEW = 'review',
}

enum TaskStatus {
  TODO = 'todo',
  IN_PROGRESS = 'in_progress',
  DONE = 'done',
  BLOCKED = 'blocked',
}

enum TestType {
  FUNCTIONAL = 'functional',
  EDGE_CASE = 'edge_case',
  PERFORMANCE = 'performance',
  SECURITY = 'security',
  USABILITY = 'usability',
}

enum TestStatus {
  NOT_EXECUTED = 'not_executed',
  PASSED = 'passed',
  FAILED = 'failed',
  BLOCKED = 'blocked',
}

enum LinkType {
  DERIVED_FROM = 'derived_from',
  DEPENDS_ON = 'depends_on',
  VERIFIED_BY = 'verified_by',
  IMPLEMENTS = 'implements',
}

enum QuestionType {
  OPEN_ENDED = 'open_ended',
  CLOSED = 'closed',
  SCALE = 'scale',
  MULTIPLE_CHOICE = 'multiple_choice',
}

enum Severity {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

interface StakeholderInfo {
  id: string;
  name: string;
  role: string;
  department: string;
}

interface Constraint {
  type: string;
  description: string;
  impact: string;
}

interface Risk {
  id: string;
  description: string;
  probability: number;
  impact: number;
  mitigation: string;
}

interface Traceability {
  source: string;
  testCases: string[];
  implementation: string[];
}

interface ValidationInfo {
  validated: boolean;
  validatedBy?: string;
  validatedAt?: Date;
  comments?: string;
}

interface Task {
  id: string;
  title: string;
  description: string;
  type: TaskType;
  estimatedHours: number;
  assignee: string | null;
  status: TaskStatus;
}

interface TestCase {
  id: string;
  title: string;
  description: string;
  type: TestType;
  priority: Priority;
  preconditions: string[];
  steps: TestStep[];
  expectedResult: string;
  status: TestStatus;
}

interface TestStep {
  action: string;
  expectedResult: string;
}

interface RequirementInput {
  text?: string;
  documents?: string[];
  interviews?: InterviewResult[];
  surveys?: SurveyResult[];
}

interface UserStoryInput {
  title: string;
  asA: string;
  iWant: string;
  soThat: string;
  acceptanceCriteria?: Array<{
    given: string;
    when: string;
    then: string;
  }>;
  priority?: Priority;
  storyPoints?: number;
  epic?: string;
  sprint?: string;
  dependencies?: string[];
  notes?: string;
}

interface RequirementAnalysis {
  requirements: Requirement[];
  stakeholders: Stakeholder[];
  completeness: CompletenessAnalysis;
  consistency: ConsistencyAnalysis;
  conflicts: Conflict[];
  feasibility: FeasibilityAnalysis;
  recommendations: string[];
  traceabilityMatrix: any;
}

interface Stakeholder {
  id: string;
  name: string;
  role: string;
  department: string;
  influence: number;
  interest: number;
  requirements: string[];
}

interface CompletenessAnalysis {
  score: number;
  missingElements: string[];
  recommendations: string[];
}

interface ConsistencyAnalysis {
  isConsistent: boolean;
  issues: ConsistencyIssue[];
  score: number;
}

interface ConsistencyIssue {
  type: string;
  requirementIds: string[];
  description: string;
  severity: Severity;
}

interface Conflict {
  requirements: string[];
  description: string;
  resolution?: string;
}

interface FeasibilityAnalysis {
  isFeasible: boolean;
  risks: Risk[];
  constraints: Constraint[];
  recommendations: string[];
}

interface InterviewResult {
  stakeholder: Stakeholder;
  date: Date;
  responses: InterviewResponse[];
  insights: string[];
  actionItems: string[];
}

interface InterviewResponse {
  question: Question;
  answer: string;
  followUps: Question[];
}

interface Question {
  id: string;
  text: string;
  type: QuestionType;
  category: string;
}

interface SurveyResult {
  responses: any[];
  summary: any;
}

interface TraceLink {
  from: string;
  to: string;
  type: LinkType;
  created: Date;
}

interface ValidationRule {
  id: string;
  name: string;
  check: (req: Requirement) => boolean;
  message: string;
}

// Export the analyzer
export { RequirementsAnalyzer, Requirement, UserStory };
```

## Example 2

```markdown
# Software Requirements Specification (SRS)

## 1. Introduction
### 1.1 Purpose
[Purpose of this document]

### 1.2 Scope
[Scope of the system]

### 1.3 Definitions, Acronyms, and Abbreviations
[Key terms and definitions]

### 1.4 References
[Referenced documents]

## 2. Overall Description
### 2.1 Product Perspective
[How the product fits into the larger system]

### 2.2 Product Functions
[Major functions the product will perform]

### 2.3 User Classes and Characteristics
[Different types of users and their characteristics]

### 2.4 Operating Environment
[Hardware, software, and network environment]

### 2.5 Design and Implementation Constraints
[Limitations and constraints]

### 2.6 Assumptions and Dependencies
[Assumptions made and external dependencies]

## 3. Functional Requirements
### 3.1 Feature 1
**ID**: FR-001
**Description**: [Detailed description]
**Priority**: [Critical/High/Medium/Low]
**Acceptance Criteria**:
- [Criterion 1]
- [Criterion 2]

### 3.2 Feature 2
[Continue for all features]

## 4. Non-Functional Requirements
### 4.1 Performance Requirements
[Response times, throughput, capacity]

### 4.2 Security Requirements
[Authentication, authorization, data protection]

### 4.3 Usability Requirements
[User interface, accessibility, documentation]

### 4.4 Reliability Requirements
[Availability, fault tolerance, recovery]

## 5. System Models
### 5.1 Use Case Diagrams
[Use case diagrams]

### 5.2 Sequence Diagrams
[Sequence diagrams]

### 5.3 Data Models
[Entity relationship diagrams]

## 6. Traceability Matrix
[Requirements to test cases mapping]

## 7. Appendices
[Additional supporting information]
```
