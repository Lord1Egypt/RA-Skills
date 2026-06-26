// btw Command - Local Implementation
// Runs entirely in the agent, no external API calls

interface BtwInput {
  question: string;
  options?: string[];
  default?: string;
  timeout?: number;
  priority?: 'urgent' | 'normal' | 'low';
  context?: Record<string, any>;
}

interface BtwOutput {
  answer: string;
  answered_at: string;
  timed_out: boolean;
  response_time_ms: number;
}

// Simple in-memory question queue (for local mode)
const questionQueue: Map<string, {
  question: string;
  options: string[];
  default: string;
  timeout: number;
  priority: string;
  context: Record<string, any>;
  createdAt: number;
  expiresAt: number;
  answer?: string;
  answeredAt?: number;
}> = new Map();

export async function run(input: BtwInput): Promise<BtwOutput> {
  const startTime = Date.now();
  
  // Validate input
  if (!input.question || typeof input.question !== 'string' || input.question.trim() === '') {
    throw new Error('Missing required field: question (non-empty string)');
  }
  
  // Set defaults
  const timeout = Math.min(input.timeout || 300, 3600); // Max 1 hour
  const priority = input.priority || 'normal';
  const options = input.options || [];
  const defaultAnswer = input.default || (options.length > 0 ? options[0] : 'yes');
  const context = input.context || {};
  
  // Create question ID
  const questionId = `q_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  // Store question in memory
  const now = Date.now();
  questionQueue.set(questionId, {
    question: input.question,
    options,
    default: defaultAnswer,
    timeout,
    priority,
    context,
    createdAt: now,
    expiresAt: now + (timeout * 1000)
  });
  
  // Log question (for user to see in console/logs)
  console.log(`[btw] Question ${questionId}:`);
  console.log(`  Priority: ${priority}`);
  console.log(`  Question: ${input.question}`);
  if (options.length > 0) {
    console.log(`  Options: ${options.join(', ')}`);
  }
  console.log(`  Default: ${defaultAnswer}`);
  console.log(`  Timeout: ${timeout}s`);
  if (Object.keys(context).length > 0) {
    console.log(`  Context:`, context);
  }
  
  // Wait for answer or timeout
  const result = await waitForAnswer(questionId, timeout, defaultAnswer);
  
  const responseTime = Date.now() - startTime;
  
  // Clean up
  questionQueue.delete(questionId);
  
  return {
    answer: result.answer,
    answered_at: result.answered_at,
    timed_out: result.timed_out,
    response_time_ms: responseTime
  };
}

async function waitForAnswer(
  questionId: string,
  timeout: number,
  defaultAnswer: string
): Promise<{
  answer: string;
  answered_at: string;
  timed_out: boolean;
}> {
  const startTime = Date.now();
  const pollInterval = 1000; // Poll every 1 second
  
  while (true) {
    const question = questionQueue.get(questionId);
    
    if (!question) {
      // Question was deleted or doesn't exist
      return {
        answer: defaultAnswer,
        answered_at: new Date().toISOString(),
        timed_out: true
      };
    }
    
    // Check if answered
    if (question.answer) {
      return {
        answer: question.answer,
        answered_at: new Date(question.answeredAt!).toISOString(),
        timed_out: false
      };
    }
    
    // Check if expired
    const elapsed = Date.now() - startTime;
    if (elapsed >= timeout * 1000) {
      return {
        answer: defaultAnswer,
        answered_at: new Date().toISOString(),
        timed_out: true
      };
    }
    
    // Wait before next poll
    await new Promise(resolve => setTimeout(resolve, pollInterval));
  }
}

// Helper function to answer a question (can be called externally)
export function answerQuestion(questionId: string, answer: string): boolean {
  const question = questionQueue.get(questionId);
  
  if (!question) {
    return false;
  }
  
  // Validate answer against options
  if (question.options.length > 0 && !question.options.includes(answer)) {
    throw new Error(`Invalid answer. Must be one of: ${question.options.join(', ')}`);
  }
  
  question.answer = answer;
  question.answeredAt = Date.now();
  
  return true;
}

// Helper function to list pending questions
export function listPendingQuestions(): Array<{
  id: string;
  question: string;
  options: string[];
  default: string;
  priority: string;
  context: Record<string, any>;
  timeRemaining: number;
}> {
  const now = Date.now();
  const pending: Array<any> = [];
  
  for (const [id, q] of questionQueue.entries()) {
    if (!q.answer && q.expiresAt > now) {
      pending.push({
        id,
        question: q.question,
        options: q.options,
        default: q.default,
        priority: q.priority,
        context: q.context,
        timeRemaining: Math.floor((q.expiresAt - now) / 1000)
      });
    }
  }
  
  return pending;
}

export default run;
