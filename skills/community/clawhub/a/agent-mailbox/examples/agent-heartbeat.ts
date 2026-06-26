/**
 * Example: Agent Heartbeat with Mailbox Processing
 * 
 * This example shows how to integrate mailbox into your agent's
 * heartbeat routine to process incoming tasks and messages.
 * 
 * Use as a cron job that runs every 5 minutes:
 * openclaw cron add --schedule "every 5 minutes" --task "node agent-heartbeat.js"
 */

import { Mailbox } from '../src/lib/mailbox';

/**
 * Main heartbeat function
 */
async function agentHeartbeat() {
  const agentName = process.env.AGENT_NAME || 'pinchie';
  const mail = new Mailbox(agentName);

  console.log(`[${new Date().toISOString()}] Heartbeat started`);

  try {
    // 1. Get urgent messages
    const urgent = await mail.getUrgent();
    console.log(`Found ${urgent.length} urgent messages`);

    for (const msg of urgent) {
      console.log(`\n[URGENT] Processing message from ${msg.from}`);
      console.log(`Subject: ${msg.subject}`);

      // 2. Check if it's a task
      if (msg.metadata?.task_id) {
        console.log(`Task ID: ${msg.metadata.task_id}`);

        try {
          // 3. Execute the task (your custom logic here)
          const taskResult = await executeTask(msg.metadata.task_id, msg);

          // 4. Reply with results
          await mail.reply(
            msg.id,
            `Task complete!\n\nResult:\n${taskResult}`,
            { status: 'completed' }
          );

          console.log(`✓ Task ${msg.metadata.task_id} completed`);

          // 5. Optionally call a webhook callback
          if (msg.metadata?.callback_url) {
            await callWebhook(msg.metadata.callback_url, {
              task_id: msg.metadata.task_id,
              status: 'completed',
              result: taskResult,
            });
          }
        } catch (error) {
          // Handle task error
          console.error(`✗ Task failed: ${error}`);

          await mail.reply(
            msg.id,
            `Task failed with error:\n\n${error}`,
            { status: 'failed', error: String(error) }
          );
        }
      } else {
        // Not a task, just a message
        console.log(`Regular message: ${msg.subject}`);
        // Your custom handling here
      }

      // Mark as read
      await mail.markRead(msg.id);
    }

    // 6. Clean up expired messages
    const archived = await mail.archiveExpired();
    if (archived > 0) {
      console.log(`\nArchived ${archived} expired messages`);
    }

    // 7. Report stats
    const stats = await mail.getStats();
    console.log(`\nMailbox stats: ${stats.unread} unread, ${stats.high_priority} high-priority`);

    console.log(`\nHeartbeat complete`);
  } catch (error) {
    console.error(`Heartbeat error: ${error}`);
    process.exit(1);
  }
}

/**
 * Example task execution function
 * Replace with your actual task logic
 */
async function executeTask(taskId: string, msg: any): Promise<string> {
  console.log(`[TASK] Executing task: ${taskId}`);

  // Example: Crypto analysis task
  if (taskId.startsWith('crypto-')) {
    return `Analysis complete for ${taskId}:
- BTC/USDT correlation: 0.89
- 24h volume: $45.2B
- Sentiment: Bullish`;
  }

  // Example: Web scraping task
  if (taskId.startsWith('scrape-')) {
    return `Scraped data from URL:
- Title: Example Page
- Content: 250 words extracted
- Links found: 12`;
  }

  // Example: Default task
  return `Task ${taskId} executed successfully`;
}

/**
 * Example webhook callback
 */
async function callWebhook(
  url: string,
  payload: Record<string, any>
): Promise<void> {
  console.log(`[WEBHOOK] Calling ${url}`);

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      console.warn(`Webhook returned ${response.status}`);
    } else {
      console.log(`Webhook success`);
    }
  } catch (error) {
    console.warn(`Webhook failed: ${error}`);
    // Don't fail the heartbeat if webhook fails
  }
}

// Run heartbeat
agentHeartbeat().catch(console.error);
