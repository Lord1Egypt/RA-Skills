/**
 * 通讯录管理模块
 * 支持搜索联系人、查询部门成员
 */

const { DWSClient } = require('./dws');

class ContactClient {
  constructor(options = {}) {
    this.dws = new DWSClient(options);
  }

  /**
   * 搜索联系人
   * @param {Object} params - 搜索参数
   * @param {string} params.name - 按姓名搜索
   * @param {string} params.dept - 按部门搜索
   * @param {string} params.keyword - 通用关键词搜索
   * @returns {Array} 联系人列表
   */
  async search(params = {}) {
    const args = [];

    if (params.name) {
      args.push('--name', params.name);
    } else if (params.dept) {
      args.push('--dept', params.dept);
    } else if (params.keyword) {
      args.push('--keyword', params.keyword);
    }

    const result = this.dws.exec('contact', ['search', ...args]);
    
    // 格式化返回数据
    if (result.contacts && Array.isArray(result.contacts)) {
      return result.contacts.map(contact => ({
        id: contact.id || contact.userid,
        name: contact.name,
        email: contact.email,
        phone: contact.mobile || contact.phone,
        dept: contact.department || contact.dept,
        title: contact.title || contact.position,
        avatar: contact.avatar
      }));
    }
    
    return result;
  }

  /**
   * 获取部门成员列表
   * @param {string} deptId - 部门ID
   * @param {boolean} includeSubDepts - 是否包含子部门
   * @returns {Array} 成员列表
   */
  async getDeptMembers(deptId, includeSubDepts = false) {
    if (!deptId) {
      throw new Error('部门ID不能为空');
    }

    const args = ['--dept-id', deptId];
    if (includeSubDepts) {
      args.push('--include-sub');
    }

    const result = this.dws.exec('contact', ['dept-members', ...args]);
    
    if (result.members && Array.isArray(result.members)) {
      return result.members.map(member => ({
        id: member.id || member.userid,
        name: member.name,
        email: member.email,
        phone: member.mobile || member.phone,
        title: member.title || member.position,
        leader: member.isLeader || false
      }));
    }
    
    return result;
  }

  /**
   * 获取部门列表
   * @returns {Array} 部门列表
   */
  async listDepartments() {
    const result = this.dws.exec('contact', ['list-depts']);
    
    if (result.departments && Array.isArray(result.departments)) {
      return result.departments.map(dept => ({
        id: dept.id,
        name: dept.name,
        parentId: dept.parentid,
        order: dept.order,
        memberCount: dept.memberCount
      }));
    }
    
    return result;
  }

  /**
   * 获取用户详情
   * @param {string} userId - 用户ID
   * @returns {Object} 用户详情
   */
  async getUserDetail(userId) {
    if (!userId) {
      throw new Error('用户ID不能为空');
    }

    const result = this.dws.exec('contact', ['user-detail', '--id', userId]);
    
    if (result.user) {
      const user = result.user;
      return {
        id: user.id || user.userid,
        name: user.name,
        email: user.email,
        phone: user.mobile || user.phone,
        dept: user.department || user.dept,
        title: user.title || user.position,
        avatar: user.avatar,
        hiredDate: user.hiredDate,
        jobNumber: user.jobnumber
      };
    }
    
    return result;
  }

  /**
   * 获取当前用户信息
   * @returns {Object} 当前用户信息
   */
  async getCurrentUser() {
    const result = this.dws.exec('contact', ['me']);
    
    if (result.user) {
      const user = result.user;
      return {
        id: user.id || user.userid,
        name: user.name,
        email: user.email,
        phone: user.mobile || user.phone,
        dept: user.department || user.dept,
        title: user.title || user.position
      };
    }
    
    return result;
  }
}

module.exports = ContactClient;