#!/usr/bin/env node

/**
 * 更新设计系统元数据脚本
 * 基于实际的 DESIGN.md 文件内容自动生成元数据
 */

const fs = require('fs');
const path = require('path');

// 配置文件路径
const CONFIG_PATH = path.join(__dirname, '../config/design-mapping.yaml');
const DESIGN_SYSTEMS_PATH = path.join(__dirname, '../design-systems');

// 读取 YAML 配置（简单解析）
function parseYaml(yaml) {
  const lines = yaml.split('\n');
  let inDesignSystems = false;
  let currentSystem = null;
  const designSystems = {};

  for (const line of lines) {
    if (line.trim() === 'designSystems:') {
      inDesignSystems = true;
      continue;
    }
    
    if (inDesignSystems) {
      const systemMatch = line.match(/^  (\w+):$/);
      if (systemMatch) {
        currentSystem = systemMatch[1];
        designSystems[currentSystem] = {};
      } else if (currentSystem && line.includes(':')) {
        const kvMatch = line.match(/\s+(\w+):\s*(.+)/);
        if (kvMatch) {
          let value = kvMatch[2].trim();
          if (value === 'true') value = true;
          else if (value === 'false') value = false;
          designSystems[currentSystem][kvMatch[1]] = value;
        }
      }
    }
  }

  return designSystems;
}

// 写入 YAML 配置（简单生成）
function generateYaml(config) {
  let yaml = '';
  
  // 复制原配置的头部
  const originalConfig = fs.readFileSync(CONFIG_PATH, 'utf8');
  const headerLines = originalConfig.split('\n').slice(0, originalConfig.indexOf('designSystems:'));
  yaml += headerLines.join('\n') + '\n';
  
  // 添加 designSystems
  yaml += 'designSystems:\n';
  for (const [name, meta] of Object.entries(config.designSystems)) {
    yaml += `  ${name}:\n`;
    yaml += `    name: "${meta.name}"\n`;
    yaml += `    description: "${meta.description}"\n`;
    const tagsArray = Array.isArray(meta.tags) ? meta.tags : [];
    yaml += `    tags: [${tagsArray.map(tag => `"${tag}"`).join(', ')}]\n`;
    yaml += `    primaryColor: "${meta.primaryColor}"\n`;
    yaml += `    darkMode: ${meta.darkMode}\n`;
  }
  
  return yaml;
}

// 从 DESIGN.md 提取元数据
function extractMetadata(designSystemName) {
  try {
    const designMdPath = path.join(DESIGN_SYSTEMS_PATH, designSystemName, 'DESIGN.md');
    if (!fs.existsSync(designMdPath)) {
      console.log(`⚠️  ${designSystemName}/DESIGN.md not found`);
      return null;
    }
    
    const content = fs.readFileSync(designMdPath, 'utf8');
    
    // 提取标题和描述
    const titleMatch = content.match(/^# Design System Inspiration of (.+)$/m);
    const name = titleMatch ? titleMatch[1] : designSystemName;
    
    const descMatch = content.match(/^## 1\. Visual Theme & Atmosphere\s*\n\n(.+?)(?:\n\n##|\n$)/s);
    const description = descMatch ? descMatch[1].replace(/\n/g, ' ').substring(0, 100) + '...' : `${name} design system`;
    
    // 简单的颜色检测（基于常见模式）
    let primaryColor = '#000000';
    let darkMode = false;
    
    if (content.includes('#5e6ad2') || content.includes('#5E6AD2')) {
      primaryColor = '#5E6AD2';
      darkMode = true;
    } else if (content.includes('#533afd') || content.includes('#533AFD')) {
      primaryColor = '#533AFD';
      darkMode = false;
    } else if (content.includes('dark') || content.includes('black') || content.includes('#08090a')) {
      darkMode = true;
    }
    
    // 标签推断
    const tags = [];
    const lowerContent = content.toLowerCase();
    if (lowerContent.includes('saas') || lowerContent.includes('productivity')) tags.push('saas', 'productivity');
    if (lowerContent.includes('payment') || lowerContent.includes('finance')) tags.push('payment', 'finance');
    if (lowerContent.includes('marketing') || lowerContent.includes('brand')) tags.push('marketing', 'brand');
    if (lowerContent.includes('mobile') || lowerContent.includes('ios')) tags.push('mobile', 'consumer');
    if (lowerContent.includes('music') || lowerContent.includes('audio')) tags.push('entertainment', 'music');
    if (lowerContent.includes('ai') || lowerContent.includes('artificial intelligence')) tags.push('ai', 'tech');
    if (lowerContent.includes('developer') || lowerContent.includes('code')) tags.push('dev-tools', 'developer');
    if (lowerContent.includes('design') || lowerContent.includes('creative')) tags.push('design', 'creative');
    if (lowerContent.includes('database') || lowerContent.includes('infrastructure')) tags.push('infrastructure', 'database');
    if (lowerContent.includes('monitoring') || lowerContent.includes('dashboard')) tags.push('monitoring', 'dashboard');
    
    return {
      name,
      description,
      tags: [...new Set(tags)], // 去重
      primaryColor,
      darkMode
    };
  } catch (error) {
    console.error(`❌ Error extracting metadata for ${designSystemName}:`, error.message);
    return null;
  }
}

// 主函数
async function main() {
  console.log('🔄 Updating design systems metadata...');
  
  // 读取现有配置
  const configContent = fs.readFileSync(CONFIG_PATH, 'utf8');
  const existingDesignSystems = parseYaml(configContent);
  
  // 获取所有设计系统目录
  const designSystemDirs = fs.readdirSync(DESIGN_SYSTEMS_PATH).filter(dir => 
    fs.statSync(path.join(DESIGN_SYSTEMS_PATH, dir)).isDirectory()
  );
  
  console.log(`📊 Found ${designSystemDirs.length} design systems`);
  
  // 更新元数据
  const updatedDesignSystems = { ...existingDesignSystems };
  
  for (const dir of designSystemDirs) {
    const metadata = extractMetadata(dir);
    if (metadata) {
      updatedDesignSystems[dir] = metadata;
      console.log(`✅ Updated ${dir}`);
    }
  }
  
  // 保存更新后的配置
  const newConfig = generateYaml({ designSystems: updatedDesignSystems });
  fs.writeFileSync(CONFIG_PATH, newConfig);
  
  console.log('✅ Design systems metadata updated successfully!');
  console.log(`📄 Config file: ${CONFIG_PATH}`);
}

// 运行主函数
if (require.main === module) {
  main().catch(console.error);
}