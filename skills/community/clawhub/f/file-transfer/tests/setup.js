// Jest setup file

// Global test setup
beforeAll(() => {
  // Setup global mocks or configurations
  console.log('Setting up test environment...');
});

afterAll(() => {
  // Cleanup after all tests
  console.log('Cleaning up test environment...');
});

// Global test utilities
global.testUtils = {
  createMockFile: (size = 1024) => {
    return Buffer.alloc(size, 'test');
  },
  createMockContext: () => ({
    filePath: '/tmp/test.txt',
    fileName: 'test.txt',
    fileSize: 1024,
    fileType: 'text/plain',
    caption: 'Test file',
    chatInfo: { isGroupChat: false, chatType: 'private' },
    userInfo: { id: 'test-user', name: 'Test User' },
    channelInfo: { type: 'telegram', id: 'test-channel' },
    history: []
  })
};