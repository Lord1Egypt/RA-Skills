Page({
  data: {
    records: []
  },

  onLoad() {
    this.loadRecords();
  },

  onShow() {
    this.loadRecords();
  },

  loadRecords() {
    const that = this;
    
    wx.showLoading({ title: '加载中...' });

    wx.cloud.callFunction({
      name: 'getRedPackets',
      data: {
        limit: 50
      },
      success: function(res) {
        wx.hideLoading();
        console.log('记录列表:', res.result);
        
        // 格式化时间
        const records = (res.result.data || []).map(item => {
          const date = new Date(item.createTime);
          item.createTime = `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
          return item;
        });
        
        that.setData({ records });
      },
      fail: function(err) {
        wx.hideLoading();
        console.error('加载失败:', err);
        wx.showToast({ title: '加载失败', icon: 'none' });
      }
    });
  }
})
