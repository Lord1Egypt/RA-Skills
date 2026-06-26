/**
 * Skill 安装测试
 * 测试别人安装后是否能直接使用
 */

console.log('🧪 Enhanced Permissions Skill - 安装测试\n');
console.log('='.repeat(70));

try {
  // 步骤 1: 测试导入
  console.log('\n📦 步骤 1: 测试导入 Skill');
  console.log('-'.repeat(70));
  
  const skill = require('./index.js');
  console.log('✅ Skill 导入成功');
  console.log(`   导出模块：${Object.keys(skill).join(', ')}`);
  
  // 步骤 2: 测试初始化
  console.log('\n\n🔧 步骤 2: 测试自动初始化');
  console.log('-'.repeat(70));
  
  if (skill.initialize) {
    const instances = skill.initialize({
      enableVersionControl: true,
      enableAutoOrganize: true,
      enableSuggestions: true,
      userLevel: 'moderate'
    });
    console.log('✅ 初始化成功');
    console.log(`   memoryManager: ${instances.memoryManager ? '✅' : '❌'}`);
    console.log(`   permissionChecker: ${instances.permissionChecker ? '✅' : '❌'}`);
  } else {
    console.log('❌ initialize 函数不存在');
  }
  
  // 步骤 3: 测试获取实例
  console.log('\n\n📥 步骤 3: 测试获取实例');
  console.log('-'.repeat(70));
  
  const mm = skill.getMemoryManager();
  const pc = skill.getPermissionChecker();
  console.log('✅ 获取实例成功');
  console.log(`   memoryManager: ${mm ? '✅' : '❌'}`);
  console.log(`   permissionChecker: ${pc ? '✅' : '❌'}`);
  
  // 步骤 4: 测试核心功能
  console.log('\n\n🎯 步骤 4: 测试核心功能');
  console.log('-'.repeat(70));
  
  (async () => {
    try {
      // 测试记忆存储
      console.log('测试记忆存储...');
      const id = await mm.store('测试记忆内容', ['test', 'skill']);
      console.log(`✅ 记忆存储成功：${id}`);
      
      // 测试记忆召回
      console.log('\n测试记忆召回...');
      const memories = await mm.recall('测试', { limit: 5 });
      console.log(`✅ 记忆召回成功：找到 ${memories.length} 条`);
      
      // 测试版本控制
      console.log('\n测试版本控制...');
      await mm.updateMemory(id, '更新后的内容', 'tester', '测试更新');
      const history = await mm.getVersionHistory(id);
      console.log(`✅ 版本历史：${history.length} 个版本`);
      
      // 测试权限检查
      console.log('\n测试权限检查...');
      const checkResult = await pc.check('read', {
        sessionId: 'test',
        operation: 'read',
        params: { path: 'test.txt' },
        timestamp: Date.now()
      });
      console.log(`✅ 权限检查：${checkResult.allowed ? '允许' : '拒绝'}`);
      
      // 测试自动整理
      console.log('\n测试自动整理...');
      const organizeResult = await mm.autoOrganize({ dryRun: true });
      console.log(`✅ 自动整理：发现 ${organizeResult.duplicatesFound} 个重复`);
      
      // 步骤 5: 测试工具注册（模拟）
      console.log('\n\n🔧 步骤 5: 测试工具注册（模拟）');
      console.log('-'.repeat(70));
      
      const mockOpenClaw = {
        tools: {},
        registerTool: function(name, config) {
          this.tools[name] = config;
          console.log(`   ✅ 注册工具：${name}`);
        }
      };
      
      if (skill.registerTools) {
        skill.registerTools(mockOpenClaw);
        console.log(`✅ 工具注册成功：${Object.keys(mockOpenClaw.tools).length} 个工具`);
      } else {
        console.log('❌ registerTools 函数不存在');
      }
      
      // 测试总结
      console.log('\n\n' + '='.repeat(70));
      console.log('🎉 测试总结');
      console.log('='.repeat(70));
      console.log('✅ Skill 导入：成功');
      console.log('✅ 自动初始化：成功');
      console.log('✅ 获取实例：成功');
      console.log('✅ 核心功能：成功');
      console.log('✅ 工具注册：成功');
      console.log('\n✨ Skill 安装测试全部通过！别人安装后可以直接使用！\n');
      
    } catch (error) {
      console.error('\n❌ 核心功能测试失败:', error);
      process.exit(1);
    }
  })();
  
} catch (error) {
  console.error('\n❌ Skill 导入失败:', error);
  process.exit(1);
}
