// {{ module_name }} 模块 API 接口
// 自动生成时间: {{ generate_time }}

import request from '@/utils/request'

{% for model in models %}
// {{ model.name }} API
export function get{{ model.name }}List(params) {
  return request({
    url: '/{{ module_name }}/{{ model.name|lower }}/',
    method: 'get',
    params
  })
}

export function get{{ model.name }}(id) {
  return request({
    url: `/{{ module_name }}/{{ model.name|lower }}/${id}/`,
    method: 'get'
  })
}

export function create{{ model.name }}(data) {
  return request({
    url: '/{{ module_name }}/{{ model.name|lower }}/',
    method: 'post',
    data
  })
}

export function update{{ model.name }}(id, data) {
  return request({
    url: `/{{ module_name }}/{{ model.name|lower }}/${id}/`,
    method: 'put',
    data
  })
}

export function delete{{ model.name }}(id) {
  return request({
    url: `/{{ module_name }}/{{ model.name|lower }}/${id}/`,
    method: 'delete'
  })
}

{% endfor %}
