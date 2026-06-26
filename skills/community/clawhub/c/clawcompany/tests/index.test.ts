import { createProject, runPMAgent, runDevAgent, runReviewAgent } from '../src/index'

describe('ClawCompany', () => {
  describe('createProject', () => {
    it('应该能创建项目', async () => {
      const result = await createProject('创建一个登录页面')
      
      expect(result).toHaveProperty('success')
      expect(result).toHaveProperty('tasks')
      expect(result).toHaveProperty('files')
      expect(result).toHaveProperty('summary')
    }, 30000)

    it('应该返回任务列表', async () => {
      const result = await createProject('创建计算器')
      
      expect(Array.isArray(result.tasks)).toBe(true)
      expect(result.tasks.length).toBeGreaterThan(0)
    }, 30000)
  })

  describe('runPMAgent', () => {
    it('应该能拆分任务', async () => {
      const tasks = await runPMAgent('创建登录页面')
      
      expect(Array.isArray(tasks)).toBe(true)
      expect(tasks.length).toBeGreaterThan(0)
      expect(tasks[0]).toHaveProperty('title')
      expect(tasks[0]).toHaveProperty('description')
    }, 15000)
  })

  describe('runDevAgent', () => {
    it('应该能生成文件', async () => {
      const task = {
        id: 'test-1',
        title: '创建组件',
        description: '创建一个简单组件',
        assignedTo: 'dev' as const,
        dependencies: []
      }
      
      const files = await runDevAgent(task, '/tmp/test-project')
      
      expect(Array.isArray(files)).toBe(true)
    }, 30000)
  })

  describe('runReviewAgent', () => {
    it('应该能审查代码', async () => {
      const task = {
        id: 'test-1',
        title: '测试任务',
        description: '测试',
        assignedTo: 'dev' as const,
        dependencies: []
      }
      
      const approved = await runReviewAgent(task, ['test.ts'])
      
      expect(typeof approved).toBe('boolean')
    }, 15000)
  })
})
