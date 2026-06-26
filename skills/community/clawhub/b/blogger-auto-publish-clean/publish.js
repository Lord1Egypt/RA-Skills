#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const { google } = require('googleapis');
const config = require('./config.js');
const BloggerAuth = require('./auth.js');

class BloggerPublisher {
  constructor() {
    this.auth = new BloggerAuth();
    this.blogger = null;
  }

  async initialize() {
    const authClient = await this.auth.authorize();
    if (!authClient) {
      throw new Error('Not authorized. Please run authorization first.');
    }
    
    this.blogger = google.blogger({
      version: 'v3',
      auth: authClient
    });
    
    console.log('✓ Blogger API initialized');
  }

  async parseMarkdownFile(filePath) {
    try {
      const content = await fs.readFile(filePath, 'utf8');
      
      // Parse frontmatter (simple version)
      const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
      
      let metadata = {
        title: path.basename(filePath, '.md'),
        labels: [],
        draft: false
      };
      
      let markdownContent = content;
      
      if (frontmatterMatch) {
        const frontmatter = frontmatterMatch[1];
        markdownContent = frontmatterMatch[2];
        
        // Parse simple key-value pairs
        const lines = frontmatter.split('\n');
        for (const line of lines) {
          const match = line.match(/^(\w+):\s*(.+)$/);
          if (match) {
            const key = match[1].trim();
            const value = match[2].trim();
            
            if (key === 'title') {
              metadata.title = value;
            } else if (key === 'labels') {
              metadata.labels = value.split(',').map(l => l.trim());
            } else if (key === 'draft') {
              metadata.draft = value.toLowerCase() === 'true';
            }
          }
        }
      }
      
      // Simple Markdown to HTML conversion
      const htmlContent = this.markdownToHtml(markdownContent);
      
      return {
        metadata,
        htmlContent
      };
    } catch (error) {
      console.error('Error parsing markdown file:', error.message);
      throw error;
    }
  }

  markdownToHtml(markdown) {
    // Simple Markdown to HTML conversion
    let html = markdown
      // Headers
      .replace(/^# (.*$)/gm, '<h1>$1</h1>')
      .replace(/^## (.*$)/gm, '<h2>$1</h2>')
      .replace(/^### (.*$)/gm, '<h3>$1</h3>')
      // Bold
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Italic
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      // Lists
      .replace(/^- (.*$)/gm, '<li>$1</li>')
      .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
      // Paragraphs
      .replace(/^(?!<[hlu])(.*)$/gm, '<p>$1</p>')
      // Line breaks
      .replace(/\n/g, '<br>');
    
    return html;
  }

  async publishPost(filePath, options = {}) {
    try {
      await this.initialize();
      
      const { metadata, htmlContent } = await this.parseMarkdownFile(filePath);
      
      const postData = {
        title: options.title || metadata.title,
        content: htmlContent,
        labels: options.labels || metadata.labels
      };
      
      if (options.draft !== undefined) {
        postData.status = options.draft ? 'draft' : 'live';
      } else if (metadata.draft) {
        postData.status = 'draft';
      }
      
      console.log(`📝 Publishing: ${postData.title}`);
      console.log(`📂 File: ${filePath}`);
      console.log(`📌 Labels: ${postData.labels.join(', ') || 'none'}`);
      console.log(`📄 Status: ${postData.status || 'live'}`);
      
      const response = await this.blogger.posts.insert({
        blogId: config.blogId,
        requestBody: postData
      });
      
      console.log('✅ Post published successfully!');
      console.log(`🔗 URL: ${response.data.url}`);
      console.log(`🆔 Post ID: ${response.data.id}`);
      
      return response.data;
    } catch (error) {
      console.error('❌ Error publishing post:', error.message);
      if (error.response) {
        console.error('Response:', error.response.data);
      }
      throw error;
    }
  }

  async listPosts() {
    try {
      await this.initialize();
      
      const response = await this.blogger.posts.list({
        blogId: config.blogId,
        maxResults: 20
      });
      
      console.log(`📚 Posts in blog (${response.data.items?.length || 0}):`);
      console.log('='.repeat(50));
      
      if (response.data.items && response.data.items.length > 0) {
        response.data.items.forEach((post, index) => {
          console.log(`${index + 1}. ${post.title}`);
          console.log(`   ID: ${post.id}`);
          console.log(`   Status: ${post.status}`);
          console.log(`   Published: ${post.published || 'Not published'}`);
          console.log(`   URL: ${post.url || 'No URL'}`);
          console.log('   ---');
        });
      } else {
        console.log('No posts found.');
      }
      
      return response.data;
    } catch (error) {
      console.error('Error listing posts:', error.message);
      throw error;
    }
  }
}

// Command line interface
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log('Blogger Auto-Publish Tool');
    console.log('=========================');
    console.log('');
    console.log('Usage:');
    console.log('  node publish.js --file <markdown-file> [options]');
    console.log('  node publish.js --list');
    console.log('');
    console.log('Options:');
    console.log('  --file, -f      Path to Markdown file to publish');
    console.log('  --title, -t     Override post title');
    console.log('  --labels, -l    Comma-separated labels (overrides frontmatter)');
    console.log('  --draft, -d     Publish as draft (true/false)');
    console.log('  --list          List all posts in blog');
    console.log('  --help, -h      Show this help');
    console.log('');
    console.log('Examples:');
    console.log('  node publish.js --file post.md');
    console.log('  node publish.js --file post.md --title "My New Post" --draft true');
    console.log('  node publish.js --list');
    return;
  }
  
  const publisher = new BloggerPublisher();
  
  if (args.includes('--list')) {
    await publisher.listPosts();
    return;
  }
  
  const fileIndex = args.indexOf('--file') !== -1 ? args.indexOf('--file') : args.indexOf('-f');
  if (fileIndex === -1 || !args[fileIndex + 1]) {
    console.error('Error: --file option is required');
    console.log('Run: node publish.js --help for usage information');
    process.exit(1);
  }
  
  const filePath = args[fileIndex + 1];
  
  // Parse options
  const options = {};
  
  const titleIndex = args.indexOf('--title') !== -1 ? args.indexOf('--title') : args.indexOf('-t');
  if (titleIndex !== -1 && args[titleIndex + 1]) {
    options.title = args[titleIndex + 1];
  }
  
  const labelsIndex = args.indexOf('--labels') !== -1 ? args.indexOf('--labels') : args.indexOf('-l');
  if (labelsIndex !== -1 && args[labelsIndex + 1]) {
    options.labels = args[labelsIndex + 1].split(',').map(l => l.trim());
  }
  
  const draftIndex = args.indexOf('--draft') !== -1 ? args.indexOf('--draft') : args.indexOf('-d');
  if (draftIndex !== -1 && args[draftIndex + 1]) {
    options.draft = args[draftIndex + 1].toLowerCase() === 'true';
  }
  
  try {
    await publisher.publishPost(filePath, options);
  } catch (error) {
    console.error('Publication failed:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error.message);
    process.exit(1);
  });
}

module.exports = BloggerPublisher;