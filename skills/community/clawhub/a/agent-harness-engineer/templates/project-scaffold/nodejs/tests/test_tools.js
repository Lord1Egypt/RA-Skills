/**
 * 测试工具功能
 */

const { FileTools } = require('../src/tools/file_tools');
const { NetworkTools } = require('../src/tools/network_tools');

describe('FileTools', () => {
  let fileTools;
  
  beforeEach(() => {
    fileTools = new FileTools();
  });
  
  test('should read file', () => {
    const fs = require('fs');
    jest.spyOn(fs, 'readFileSync').mockReturnValue('Hello, World!');
    
    const result = fileTools.readFile({ path: 'test.txt' });
    expect(result).toBe('Hello, World!');
  });
  
  test('should write file', () => {
    const fs = require('fs');
    jest.spyOn(fs, 'writeFileSync').mockImplementation(() => {});
    jest.spyOn(fs, 'existsSync').mockReturnValue(true);
    
    const result = fileTools.writeFile({
      path: 'test.txt',
      content: 'Hello, World!'
    });
    expect(result).toContain('Successfully wrote');
  });
});

describe('NetworkTools', () => {
  let networkTools;
  
  beforeEach(() => {
    networkTools = new NetworkTools();
  });
  
  test('should make HTTP request', async () => {
    const axios = require('axios');
    jest.spyOn(axios, 'get').mockResolvedValue({
      status: 200,
      headers: {},
      data: 'OK'
    });
    
    const result = await networkTools.httpRequest({
      url: 'https://example.com',
      method: 'GET'
    });
    
    expect(result.status).toBe(200);
    expect(result.body).toBe('OK');
  });
});
