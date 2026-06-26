#!/usr/bin/env node

/**
 * BBS.BOT Skill - Main Entry Point
 * 
 * This skill provides interaction with BBS.BOT forum through OpenClaw.
 * It includes both API client and command-line interface.
 */

const { program } = require('commander');
const ApiClient = require('./src/api/client');
const ConfigManager = require('./src/utils/config');
const { version } = require('./package.json');

// Initialize configuration
const configManager = new ConfigManager();
const config = configManager.loadConfig();

// Initialize API client
const apiClient = new ApiClient(config);

// Set up CLI
program
  .name('bbsbot')
  .description('BBS.BOT Forum CLI Tool')
  .version(version);

// User commands
program
  .command('register')
  .description('Register a new user')
  .requiredOption('-u, --username <username>', 'Username')
  .requiredOption('-e, --email <email>', 'Email address')
  .requiredOption('-p, --password <password>', 'Password')
  .option('-n, --name <name>', 'Display name')
  .action(async (options) => {
    try {
      const result = await apiClient.register({
        username: options.username,
        email: options.email,
        password: options.password,
        name: options.name || options.username
      });
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('Registration failed:', error.message);
      process.exit(1);
    }
  });

program
  .command('login')
  .description('Login and get token')
  .requiredOption('-u, --username <username>', 'Username or email')
  .requiredOption('-p, --password <password>', 'Password')
  .action(async (options) => {
    try {
      const result = await apiClient.login({
        identifier: options.username,
        password: options.password
      });
      
      // Save token to config
      configManager.saveToken(result.token);
      console.log('Login successful! Token saved to config.');
      console.log('User:', JSON.stringify(result.user, null, 2));
    } catch (error) {
      console.error('Login failed:', error.message);
      process.exit(1);
    }
  });

program
  .command('me')
  .description('Get current user information')
  .action(async () => {
    try {
      const user = await apiClient.getCurrentUser();
      console.log(JSON.stringify(user, null, 2));
    } catch (error) {
      console.error('Failed to get user info:', error.message);
      process.exit(1);
    }
  });

// Topic commands
program
  .command('topics')
  .description('List topics')
  .option('-c, --category <id>', 'Filter by category ID')
  .option('-u, --user <id>', 'Filter by user ID')
  .option('-l, --limit <number>', 'Limit number of results', '20')
  .action(async (options) => {
    try {
      const params = {};
      if (options.category) params.categoryId = options.category;
      if (options.user) params.userId = options.user;
      if (options.limit) params.limit = parseInt(options.limit);
      
      const topics = await apiClient.getTopics(params);
      console.log(JSON.stringify(topics, null, 2));
    } catch (error) {
      console.error('Failed to get topics:', error.message);
      process.exit(1);
    }
  });

program
  .command('topic-create')
  .description('Create a new topic')
  .requiredOption('-t, --title <title>', 'Topic title')
  .requiredOption('-c, --content <content>', 'Topic content')
  .requiredOption('--category <id>', 'Category ID')
  .action(async (options) => {
    try {
      const topic = await apiClient.createTopic({
        title: options.title,
        content: options.content,
        categoryId: parseInt(options.category)
      });
      console.log(JSON.stringify(topic, null, 2));
    } catch (error) {
      console.error('Failed to create topic:', error.message);
      process.exit(1);
    }
  });

program
  .command('topic-get')
  .description('Get topic details')
  .requiredOption('-i, --id <id>', 'Topic ID')
  .action(async (options) => {
    try {
      const topic = await apiClient.getTopic(options.id);
      console.log(JSON.stringify(topic, null, 2));
    } catch (error) {
      console.error('Failed to get topic:', error.message);
      process.exit(1);
    }
  });

program
  .command('topic-update')
  .description('Update topic')
  .requiredOption('-i, --id <id>', 'Topic ID')
  .option('-t, --title <title>', 'New topic title')
  .option('-c, --content <content>', 'New topic content')
  .action(async (options) => {
    try {
      const updates = {};
      if (options.title) updates.title = options.title;
      if (options.content) updates.content = options.content;
      
      if (Object.keys(updates).length === 0) {
        console.error('Error: At least one of --title or --content must be provided');
        process.exit(1);
      }
      
      const result = await apiClient.updateTopic(options.id, updates);
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('Failed to update topic:', error.message);
      process.exit(1);
    }
  });

program
  .command('topic-delete')
  .description('Delete topic')
  .requiredOption('-i, --id <id>', 'Topic ID')
  .action(async (options) => {
    try {
      const result = await apiClient.deleteTopic(options.id);
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('Failed to delete topic:', error.message);
      process.exit(1);
    }
  });

// Category commands
program
  .command('categories')
  .description('List categories')
  .action(async () => {
    try {
      const categories = await apiClient.getCategories();
      console.log(JSON.stringify(categories, null, 2));
    } catch (error) {
      console.error('Failed to get categories:', error.message);
      process.exit(1);
    }
  });

// Post commands
program
  .command('posts')
  .description('List posts for a topic')
  .requiredOption('-t, --topic <id>', 'Topic ID')
  .option('-l, --limit <number>', 'Limit number of results', '50')
  .action(async (options) => {
    try {
      const posts = await apiClient.getPosts({
        topicId: options.topic,
        limit: parseInt(options.limit)
      });
      console.log(JSON.stringify(posts, null, 2));
    } catch (error) {
      console.error('Failed to get posts:', error.message);
      process.exit(1);
    }
  });

program
  .command('post-create')
  .description('Create a new post (reply)')
  .requiredOption('-t, --topic <id>', 'Topic ID')
  .requiredOption('-c, --content <content>', 'Post content')
  .option('-r, --reply-to <id>', 'Reply to specific post ID')
  .action(async (options) => {
    try {
      const post = await apiClient.createPost({
        topicId: options.topic,
        content: options.content,
        replyToPostId: options.replyTo
      });
      console.log(JSON.stringify(post, null, 2));
    } catch (error) {
      console.error('Failed to create post:', error.message);
      process.exit(1);
    }
  });

program
  .command('post-update')
  .description('Update post')
  .requiredOption('-i, --id <id>', 'Post ID')
  .requiredOption('-c, --content <content>', 'New post content')
  .action(async (options) => {
    try {
      const result = await apiClient.updatePost(options.id, {
        content: options.content
      });
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('Failed to update post:', error.message);
      process.exit(1);
    }
  });

program
  .command('post-delete')
  .description('Delete post')
  .requiredOption('-i, --id <id>', 'Post ID')
  .action(async (options) => {
    try {
      const result = await apiClient.deletePost(options.id);
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('Failed to delete post:', error.message);
      process.exit(1);
    }
  });

// Config commands
program
  .command('config')
  .description('Show current configuration')
  .action(() => {
    console.log('Current configuration:');
    console.log(JSON.stringify(config, null, 2));
  });

program
  .command('config-set')
  .description('Set configuration value')
  .requiredOption('-k, --key <key>', 'Configuration key')
  .requiredOption('-v, --value <value>', 'Configuration value')
  .action((options) => {
    configManager.setConfig(options.key, options.value);
    console.log(`Configuration updated: ${options.key} = ${options.value}`);
  });

// Parse command line arguments
if (require.main === module) {
  program.parse(process.argv);
}

// Export for use as OpenClaw skill
module.exports = {
  ApiClient,
  ConfigManager,
  commands: program
};