import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取授权码
    const authCode = localStorage.getItem('auth_code')

    if (authCode) {
      config.headers['Authorization'] = `Bearer ${authCode}`
    }

    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    const res = response.data

    // 如果返回的是文件流，直接返回
    if (response.config.responseType === 'blob') {
      return res
    }

    // 如果code不是200，则显示错误消息
    if (res.code && res.code !== 200) {
      ElMessage.error(res.msg || '请求失败')
      return Promise.reject(new Error(res.msg || '请求失败'))
    }

    return res
  },
  error => {
    let message = error.message

    if (error.response) {
      switch (error.response.status) {
        case 401:
          message = '未授权，请重新登录'
          localStorage.removeItem('auth_code')
          window.location.href = '/login'
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求地址不存在'
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          message = error.response.data?.msg || '请求失败'
      }
    }

    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export default api
