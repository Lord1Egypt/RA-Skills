---
name: "descriptions"
description: "Descriptions 描述列表 -- Element Plus Vue3 桌面端组件。Invoke when user needs Descriptions 描述列表 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/descriptions.html"
---

---

# Descriptions 描述列表 [​](#descriptions-描述列表)

更新日志待解决

9

列表形式展示多个字段。

## 基础用法 [​](#基础用法)

User Info

<table class="el-descriptions__table"><tbody><tr><td style="width:;min-width:;" class="el-descriptions__cell"><span style="" class="el-descriptions__label">Username</span><span class="el-descriptions__content">kooriookami</span></td><td style="width:;min-width:;" class="el-descriptions__cell"><span style="" class="el-descriptions__label">Telephone</span><span class="el-descriptions__content">18100000000</span></td><td style="width:;min-width:;" class="el-descriptions__cell"><span style="" class="el-descriptions__label">Place</span><span class="el-descriptions__content">Suzhou</span></td></tr><tr><td style="width:;min-width:;" class="el-descriptions__cell"><span style="" class="el-descriptions__label">Remarks</span><span class="el-descriptions__content"><span class="el-tag el-tag--primary el-tag--small el-tag--light" style=""><span class="el-tag__content">School</span></span></span></td><td style="width:;min-width:;" class="el-descriptions__cell" colspan="2"><span style="" class="el-descriptions__label">Address</span><span class="el-descriptions__content"> No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province</span></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZGVzY3JpcHRpb25zIHRpdGxlPVwiVXNlciBJbmZvXCI+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiVXNlcm5hbWVcIj5rb29yaW9va2FtaTwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiVGVsZXBob25lXCI+MTgxMDAwMDAwMDA8L2VsLWRlc2NyaXB0aW9ucy1pdGVtPlxuICAgIDxlbC1kZXNjcmlwdGlvbnMtaXRlbSBsYWJlbD1cIlBsYWNlXCI+U3V6aG91PC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJSZW1hcmtzXCI+XG4gICAgICA8ZWwtdGFnIHNpemU9XCJzbWFsbFwiPlNjaG9vbDwvZWwtdGFnPlxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiQWRkcmVzc1wiPlxuICAgICAgTm8uMTE4OCwgV3V6aG9uZyBBdmVudWUsIFd1emhvbmcgRGlzdHJpY3QsIFN1emhvdSwgSmlhbmdzdSBQcm92aW5jZVxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gIDwvZWwtZGVzY3JpcHRpb25zPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/descriptions/basic-usage.vue)_

vue

```
<template>
  <el-descriptions title="User Info">
    <el-descriptions-item label="Username">kooriookami</el-descriptions-item>
    <el-descriptions-item label="Telephone">18100000000</el-descriptions-item>
    <el-descriptions-item label="Place">Suzhou</el-descriptions-item>
    <el-descriptions-item label="Remarks">
      <el-tag size="small">School</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="Address">
      No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
    </el-descriptions-item>
  </el-descriptions>
</template>
```

隐藏源代码

## 不同尺寸 [​](#不同尺寸)

LargeDefaultSmall

With border

Operation

<table class="el-descriptions__table is-bordered"><tbody><tr><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1"><div class="cell-item" data-v-6630171f=""><i class="el-icon" style="margin-right:6px;" data-v-6630171f=""><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-6630171f=""><path fill="currentColor" d="M512 512a192 192 0 1 0 0-384 192 192 0 0 0 0 384m0 64a256 256 0 1 1 0-512 256 256 0 0 1 0 512m320 320v-96a96 96 0 0 0-96-96H288a96 96 0 0 0-96 96v96a32 32 0 1 1-64 0v-96a160 160 0 0 1 160-160h448a160 160 0 0 1 160 160v96a32 32 0 1 1-64 0"></path></svg></i>Username</div></td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="NaN">kooriookami</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1"><div class="cell-item" data-v-6630171f=""><i class="el-icon" style="margin-right:6px;" data-v-6630171f=""><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-6630171f=""><path fill="currentColor" d="M224 768v96.064a64 64 0 0 0 64 64h448a64 64 0 0 0 64-64V768zm0-64h576V160a64 64 0 0 0-64-64H288a64 64 0 0 0-64 64zm32 288a96 96 0 0 1-96-96V128a96 96 0 0 1 96-96h512a96 96 0 0 1 96 96v768a96 96 0 0 1-96 96zm304-144a48 48 0 1 1-96 0 48 48 0 0 1 96 0"></path></svg></i>Telephone</div></td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="NaN">18100000000</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1"><div class="cell-item" data-v-6630171f=""><i class="el-icon" style="margin-right:6px;" data-v-6630171f=""><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-6630171f=""><path fill="currentColor" d="M800 416a288 288 0 1 0-576 0c0 118.144 94.528 272.128 288 456.576C705.472 688.128 800 534.144 800 416M512 960C277.312 746.688 160 565.312 160 416a352 352 0 0 1 704 0c0 149.312-117.312 330.688-352 544"></path><path fill="currentColor" d="M512 512a96 96 0 1 0 0-192 96 96 0 0 0 0 192m0 64a160 160 0 1 1 0-320 160 160 0 0 1 0 320"></path></svg></i>Place</div></td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="NaN">Suzhou</td></tr><tr><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1"><div class="cell-item" data-v-6630171f=""><i class="el-icon" style="margin-right:6px;" data-v-6630171f=""><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-6630171f=""><path fill="currentColor" d="M192 128v768h640V128zm-32-64h704a32 32 0 0 1 32 32v832a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32m160 448h384v64H320zm0-192h192v64H320zm0 384h384v64H320z"></path></svg></i>Remarks</div></td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="NaN"><span class="el-tag el-tag--primary el-tag--small el-tag--light" style="" data-v-6630171f=""><span class="el-tag__content">School</span></span></td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1"><div class="cell-item" data-v-6630171f=""><i class="el-icon" style="margin-right:6px;" data-v-6630171f=""><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-6630171f=""><path fill="currentColor" d="M192 128v704h384V128zm-32-64h448a32 32 0 0 1 32 32v768a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32"></path><path fill="currentColor" d="M256 256h256v64H256zm0 192h256v64H256zm0 192h256v64H256zm384-128h128v64H640zm0 128h128v64H640zM64 832h896v64H64z"></path><path fill="currentColor" d="M640 384v448h192V384zm-32-64h256a32 32 0 0 1 32 32v512a32 32 0 0 1-32 32H608a32 32 0 0 1-32-32V352a32 32 0 0 1 32-32"></path></svg></i>Address</div></td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="3">No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province</td></tr></tbody></table>

Without border

Operation

<table class="el-descriptions__table"><tbody><tr><td style="width:;min-width:;" class="el-descriptions__cell"><span style="" class="el-descriptions__label">Username</span><span class="el-descriptions__content">kooriookami</span></td><td style="width:;min-width:;" class="el-descriptions__cell"><span style="" class="el-descriptions__label">Telephone</span><span class="el-descriptions__content">18100000000</span></td><td style="width:;min-width:;" class="el-descriptions__cell"><span style="" class="el-descriptions__label">Place</span><span class="el-descriptions__content">Suzhou</span></td></tr><tr><td style="width:;min-width:;" class="el-descriptions__cell"><span style="" class="el-descriptions__label">Remarks</span><span class="el-descriptions__content"><span class="el-tag el-tag--primary el-tag--small el-tag--light" style="" data-v-6630171f=""><span class="el-tag__content">School</span></span></span></td><td style="width:;min-width:;" class="el-descriptions__cell" colspan="2"><span style="" class="el-descriptions__label">Address</span><span class="el-descriptions__content"> No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province</span></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInNpemVcIj5cbiAgICA8ZWwtcmFkaW8gdmFsdWU9XCJsYXJnZVwiPkxhcmdlPC9lbC1yYWRpbz5cbiAgICA8ZWwtcmFkaW8gdmFsdWU9XCJkZWZhdWx0XCI+RGVmYXVsdDwvZWwtcmFkaW8+XG4gICAgPGVsLXJhZGlvIHZhbHVlPVwic21hbGxcIj5TbWFsbDwvZWwtcmFkaW8+XG4gIDwvZWwtcmFkaW8tZ3JvdXA+XG5cbiAgPGVsLWRlc2NyaXB0aW9uc1xuICAgIGNsYXNzPVwibWFyZ2luLXRvcFwiXG4gICAgdGl0bGU9XCJXaXRoIGJvcmRlclwiXG4gICAgOmNvbHVtbj1cIjNcIlxuICAgIDpzaXplPVwic2l6ZVwiXG4gICAgYm9yZGVyXG4gID5cbiAgICA8dGVtcGxhdGUgI2V4dHJhPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiPk9wZXJhdGlvbjwvZWwtYnV0dG9uPlxuICAgIDwvdGVtcGxhdGU+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtPlxuICAgICAgPHRlbXBsYXRlICNsYWJlbD5cbiAgICAgICAgPGRpdiBjbGFzcz1cImNlbGwtaXRlbVwiPlxuICAgICAgICAgIDxlbC1pY29uIDpzdHlsZT1cImljb25TdHlsZVwiPlxuICAgICAgICAgICAgPHVzZXIgLz5cbiAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgICAgVXNlcm5hbWVcbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAga29vcmlvb2thbWlcbiAgICA8L2VsLWRlc2NyaXB0aW9ucy1pdGVtPlxuICAgIDxlbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICAgIDx0ZW1wbGF0ZSAjbGFiZWw+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJjZWxsLWl0ZW1cIj5cbiAgICAgICAgICA8ZWwtaWNvbiA6c3R5bGU9XCJpY29uU3R5bGVcIj5cbiAgICAgICAgICAgIDxpcGhvbmUgLz5cbiAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgICAgVGVsZXBob25lXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDE4MTAwMDAwMDAwXG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgICA8dGVtcGxhdGUgI2xhYmVsPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiY2VsbC1pdGVtXCI+XG4gICAgICAgICAgPGVsLWljb24gOnN0eWxlPVwiaWNvblN0eWxlXCI+XG4gICAgICAgICAgICA8bG9jYXRpb24gLz5cbiAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgICAgUGxhY2VcbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgU3V6aG91XG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgICA8dGVtcGxhdGUgI2xhYmVsPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiY2VsbC1pdGVtXCI+XG4gICAgICAgICAgPGVsLWljb24gOnN0eWxlPVwiaWNvblN0eWxlXCI+XG4gICAgICAgICAgICA8dGlja2V0cyAvPlxuICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgICBSZW1hcmtzXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDxlbC10YWcgc2l6ZT1cInNtYWxsXCI+U2Nob29sPC9lbC10YWc+XG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgICA8dGVtcGxhdGUgI2xhYmVsPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiY2VsbC1pdGVtXCI+XG4gICAgICAgICAgPGVsLWljb24gOnN0eWxlPVwiaWNvblN0eWxlXCI+XG4gICAgICAgICAgICA8b2ZmaWNlLWJ1aWxkaW5nIC8+XG4gICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICAgIEFkZHJlc3NcbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgTm8uMTE4OCwgV3V6aG9uZyBBdmVudWUsIFd1emhvbmcgRGlzdHJpY3QsIFN1emhvdSwgSmlhbmdzdSBQcm92aW5jZVxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gIDwvZWwtZGVzY3JpcHRpb25zPlxuXG4gIDxlbC1kZXNjcmlwdGlvbnNcbiAgICBjbGFzcz1cIm1hcmdpbi10b3BcIlxuICAgIHRpdGxlPVwiV2l0aG91dCBib3JkZXJcIlxuICAgIDpjb2x1bW49XCIzXCJcbiAgICA6c2l6ZT1cInNpemVcIlxuICAgIDpzdHlsZT1cImJsb2NrTWFyZ2luXCJcbiAgPlxuICAgIDx0ZW1wbGF0ZSAjZXh0cmE+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCI+T3BlcmF0aW9uPC9lbC1idXR0b24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJVc2VybmFtZVwiPmtvb3Jpb29rYW1pPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJUZWxlcGhvbmVcIj4xODEwMDAwMDAwMDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiUGxhY2VcIj5TdXpob3U8L2VsLWRlc2NyaXB0aW9ucy1pdGVtPlxuICAgIDxlbC1kZXNjcmlwdGlvbnMtaXRlbSBsYWJlbD1cIlJlbWFya3NcIj5cbiAgICAgIDxlbC10YWcgc2l6ZT1cInNtYWxsXCI+U2Nob29sPC9lbC10YWc+XG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJBZGRyZXNzXCI+XG4gICAgICBOby4xMTg4LCBXdXpob25nIEF2ZW51ZSwgV3V6aG9uZyBEaXN0cmljdCwgU3V6aG91LCBKaWFuZ3N1IFByb3ZpbmNlXG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgPC9lbC1kZXNjcmlwdGlvbnM+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgY29tcHV0ZWQsIHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7XG4gIElwaG9uZSxcbiAgTG9jYXRpb24sXG4gIE9mZmljZUJ1aWxkaW5nLFxuICBUaWNrZXRzLFxuICBVc2VyLFxufSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuaW1wb3J0IHR5cGUgeyBDb21wb25lbnRTaXplIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBzaXplID0gcmVmPENvbXBvbmVudFNpemU+KCdkZWZhdWx0JylcblxuY29uc3QgaWNvblN0eWxlID0gY29tcHV0ZWQoKCkgPT4ge1xuICBjb25zdCBtYXJnaW5NYXAgPSB7XG4gICAgbGFyZ2U6ICc4cHgnLFxuICAgIGRlZmF1bHQ6ICc2cHgnLFxuICAgIHNtYWxsOiAnNHB4JyxcbiAgfVxuICByZXR1cm4ge1xuICAgIG1hcmdpblJpZ2h0OiBtYXJnaW5NYXBbc2l6ZS52YWx1ZV0gfHwgbWFyZ2luTWFwLmRlZmF1bHQsXG4gIH1cbn0pXG5jb25zdCBibG9ja01hcmdpbiA9IGNvbXB1dGVkKCgpID0+IHtcbiAgY29uc3QgbWFyZ2luTWFwID0ge1xuICAgIGxhcmdlOiAnMzJweCcsXG4gICAgZGVmYXVsdDogJzI4cHgnLFxuICAgIHNtYWxsOiAnMjRweCcsXG4gIH1cbiAgcmV0dXJuIHtcbiAgICBtYXJnaW5Ub3A6IG1hcmdpbk1hcFtzaXplLnZhbHVlXSB8fCBtYXJnaW5NYXAuZGVmYXVsdCxcbiAgfVxufSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmVsLWRlc2NyaXB0aW9ucyB7XG4gIG1hcmdpbi10b3A6IDIwcHg7XG59XG4uY2VsbC1pdGVtIHtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cbi5tYXJnaW4tdG9wIHtcbiAgbWFyZ2luLXRvcDogMjBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/descriptions/sizes.vue)_

vue

```
<template>
  <el-radio-group v-model="size">
    <el-radio value="large">Large</el-radio>
    <el-radio value="default">Default</el-radio>
    <el-radio value="small">Small</el-radio>
  </el-radio-group>

  <el-descriptions
    class="margin-top"
    title="With border"
    :column="3"
    :size="size"
    border
  >
    <template #extra>
      <el-button type="primary">Operation</el-button>
    </template>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <user />
          </el-icon>
          Username
        </div>
      </template>
      kooriookami
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <iphone />
          </el-icon>
          Telephone
        </div>
      </template>
      18100000000
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <location />
          </el-icon>
          Place
        </div>
      </template>
      Suzhou
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <tickets />
          </el-icon>
          Remarks
        </div>
      </template>
      <el-tag size="small">School</el-tag>
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <office-building />
          </el-icon>
          Address
        </div>
      </template>
      No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
    </el-descriptions-item>
  </el-descriptions>

  <el-descriptions
    class="margin-top"
    title="Without border"
    :column="3"
    :size="size"
    :style="blockMargin"
  >
    <template #extra>
      <el-button type="primary">Operation</el-button>
    </template>
    <el-descriptions-item label="Username">kooriookami</el-descriptions-item>
    <el-descriptions-item label="Telephone">18100000000</el-descriptions-item>
    <el-descriptions-item label="Place">Suzhou</el-descriptions-item>
    <el-descriptions-item label="Remarks">
      <el-tag size="small">School</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="Address">
      No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
    </el-descriptions-item>
  </el-descriptions>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import {
  Iphone,
  Location,
  OfficeBuilding,
  Tickets,
  User,
} from '@element-plus/icons-vue'

import type { ComponentSize } from 'element-plus'

const size = ref<ComponentSize>('default')

const iconStyle = computed(() => {
  const marginMap = {
    large: '8px',
    default: '6px',
    small: '4px',
  }
  return {
    marginRight: marginMap[size.value] || marginMap.default,
  }
})
const blockMargin = computed(() => {
  const marginMap = {
    large: '32px',
    default: '28px',
    small: '24px',
  }
  return {
    marginTop: marginMap[size.value] || marginMap.default,
  }
})
</script>

<style scoped>
.el-descriptions {
  margin-top: 20px;
}
.cell-item {
  display: flex;
  align-items: center;
}
.margin-top {
  margin-top: 20px;
}
</style>
```

隐藏源代码

## 垂直列表 [​](#垂直列表)

LargeDefaultSmall

Vertical list with border

| Username | Telephone | Place |
| --- | --- | --- |
| kooriookami | 18100000000 | Suzhou |
| Remarks | Address |
| School | No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province |

Vertical list without border

| Username | Telephone | Place |
| --- | --- | --- |
| kooriookami | 18100000000 | Suzhou |
| Remarks | Address |
| School | No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInNpemVcIj5cbiAgICA8ZWwtcmFkaW8gdmFsdWU9XCJsYXJnZVwiPkxhcmdlPC9lbC1yYWRpbz5cbiAgICA8ZWwtcmFkaW8gdmFsdWU9XCJkZWZhdWx0XCI+RGVmYXVsdDwvZWwtcmFkaW8+XG4gICAgPGVsLXJhZGlvIHZhbHVlPVwic21hbGxcIj5TbWFsbDwvZWwtcmFkaW8+XG4gIDwvZWwtcmFkaW8tZ3JvdXA+XG5cbiAgPGVsLWRlc2NyaXB0aW9uc1xuICAgIHRpdGxlPVwiVmVydGljYWwgbGlzdCB3aXRoIGJvcmRlclwiXG4gICAgZGlyZWN0aW9uPVwidmVydGljYWxcIlxuICAgIDpjb2x1bW49XCI0XCJcbiAgICA6c2l6ZT1cInNpemVcIlxuICAgIGJvcmRlclxuICA+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiVXNlcm5hbWVcIj5rb29yaW9va2FtaTwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiVGVsZXBob25lXCI+MTgxMDAwMDAwMDA8L2VsLWRlc2NyaXB0aW9ucy1pdGVtPlxuICAgIDxlbC1kZXNjcmlwdGlvbnMtaXRlbSBsYWJlbD1cIlBsYWNlXCIgOnNwYW49XCIyXCI+U3V6aG91PC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJSZW1hcmtzXCI+XG4gICAgICA8ZWwtdGFnIHNpemU9XCJzbWFsbFwiPlNjaG9vbDwvZWwtdGFnPlxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiQWRkcmVzc1wiPlxuICAgICAgTm8uMTE4OCwgV3V6aG9uZyBBdmVudWUsIFd1emhvbmcgRGlzdHJpY3QsIFN1emhvdSwgSmlhbmdzdSBQcm92aW5jZVxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gIDwvZWwtZGVzY3JpcHRpb25zPlxuXG4gIDxlbC1kZXNjcmlwdGlvbnNcbiAgICB0aXRsZT1cIlZlcnRpY2FsIGxpc3Qgd2l0aG91dCBib3JkZXJcIlxuICAgIDpjb2x1bW49XCI0XCJcbiAgICA6c2l6ZT1cInNpemVcIlxuICAgIGRpcmVjdGlvbj1cInZlcnRpY2FsXCJcbiAgICA6c3R5bGU9XCJibG9ja01hcmdpblwiXG4gID5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJVc2VybmFtZVwiPmtvb3Jpb29rYW1pPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJUZWxlcGhvbmVcIj4xODEwMDAwMDAwMDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiUGxhY2VcIiA6c3Bhbj1cIjJcIj5TdXpob3U8L2VsLWRlc2NyaXB0aW9ucy1pdGVtPlxuICAgIDxlbC1kZXNjcmlwdGlvbnMtaXRlbSBsYWJlbD1cIlJlbWFya3NcIj5cbiAgICAgIDxlbC10YWcgc2l6ZT1cInNtYWxsXCI+U2Nob29sPC9lbC10YWc+XG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJBZGRyZXNzXCI+XG4gICAgICBOby4xMTg4LCBXdXpob25nIEF2ZW51ZSwgV3V6aG9uZyBEaXN0cmljdCwgU3V6aG91LCBKaWFuZ3N1IFByb3ZpbmNlXG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgPC9lbC1kZXNjcmlwdGlvbnM+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgY29tcHV0ZWQsIHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBDb21wb25lbnRTaXplIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBzaXplID0gcmVmPENvbXBvbmVudFNpemU+KCdkZWZhdWx0JylcblxuY29uc3QgYmxvY2tNYXJnaW4gPSBjb21wdXRlZCgoKSA9PiB7XG4gIGNvbnN0IG1hcmdpbk1hcCA9IHtcbiAgICBsYXJnZTogJzMycHgnLFxuICAgIGRlZmF1bHQ6ICcyOHB4JyxcbiAgICBzbWFsbDogJzI0cHgnLFxuICB9XG4gIHJldHVybiB7XG4gICAgbWFyZ2luVG9wOiBtYXJnaW5NYXBbc2l6ZS52YWx1ZV0gfHwgbWFyZ2luTWFwLmRlZmF1bHQsXG4gIH1cbn0pXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5lbC1kZXNjcmlwdGlvbnMge1xuICBtYXJnaW4tdG9wOiAyMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/descriptions/vertical-list.vue)_

vue

```
<template>
  <el-radio-group v-model="size">
    <el-radio value="large">Large</el-radio>
    <el-radio value="default">Default</el-radio>
    <el-radio value="small">Small</el-radio>
  </el-radio-group>

  <el-descriptions
    title="Vertical list with border"
    direction="vertical"
    :column="4"
    :size="size"
    border
  >
    <el-descriptions-item label="Username">kooriookami</el-descriptions-item>
    <el-descriptions-item label="Telephone">18100000000</el-descriptions-item>
    <el-descriptions-item label="Place" :span="2">Suzhou</el-descriptions-item>
    <el-descriptions-item label="Remarks">
      <el-tag size="small">School</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="Address">
      No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
    </el-descriptions-item>
  </el-descriptions>

  <el-descriptions
    title="Vertical list without border"
    :column="4"
    :size="size"
    direction="vertical"
    :style="blockMargin"
  >
    <el-descriptions-item label="Username">kooriookami</el-descriptions-item>
    <el-descriptions-item label="Telephone">18100000000</el-descriptions-item>
    <el-descriptions-item label="Place" :span="2">Suzhou</el-descriptions-item>
    <el-descriptions-item label="Remarks">
      <el-tag size="small">School</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="Address">
      No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
    </el-descriptions-item>
  </el-descriptions>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

import type { ComponentSize } from 'element-plus'

const size = ref<ComponentSize>('default')

const blockMargin = computed(() => {
  const marginMap = {
    large: '32px',
    default: '28px',
    small: '24px',
  }
  return {
    marginTop: marginMap[size.value] || marginMap.default,
  }
})
</script>

<style scoped>
.el-descriptions {
  margin-top: 20px;
}
</style>
```

隐藏源代码

## 单元格跨行 2.8.1 [​](#单元格跨行)

Width horizontal list

<table class="el-descriptions__table is-bordered"><tbody><tr><td style="width:140px;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label is-center" colspan="1" rowspan="2">Photo</td><td style="width:140px;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content is-center" colspan="NaN" rowspan="2"><div style="width:100px;height:100px;" class="el-image"><img src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" class="el-image__inner"></div></td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1">Username</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="NaN">kooriookami</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1">Telephone</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="NaN">18100000000</td></tr><tr><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1">Place</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="NaN">Suzhou</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1">Remarks</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="NaN"><span class="el-tag el-tag--primary el-tag--small el-tag--light" style=""><span class="el-tag__content">School</span></span></td></tr><tr><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label" colspan="1">Address</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content" colspan="5">No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province</td></tr></tbody></table>

Width vertical list

| Photo | Username | Telephone |
| --- | --- | --- |
|
![](https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png)

 | kooriookami | 18100000000 |
| Place | Remarks |
| Suzhou | School |
| Address |
| No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZGVzY3JpcHRpb25zIHRpdGxlPVwiV2lkdGggaG9yaXpvbnRhbCBsaXN0XCIgYm9yZGVyPlxuICAgIDxlbC1kZXNjcmlwdGlvbnMtaXRlbVxuICAgICAgOnJvd3NwYW49XCIyXCJcbiAgICAgIDp3aWR0aD1cIjE0MFwiXG4gICAgICBsYWJlbD1cIlBob3RvXCJcbiAgICAgIGFsaWduPVwiY2VudGVyXCJcbiAgICA+XG4gICAgICA8ZWwtaW1hZ2VcbiAgICAgICAgc3R5bGU9XCJ3aWR0aDogMTAwcHg7IGhlaWdodDogMTAwcHhcIlxuICAgICAgICBzcmM9XCJodHRwczovL2N1YmUuZWxlbWVjZG4uY29tLzAvODgvMDNiMGQzOTU4M2Y0ODIwNjc2OGE3NTM0ZTU1YmNwbmcucG5nXCJcbiAgICAgIC8+XG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJVc2VybmFtZVwiPmtvb3Jpb29rYW1pPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJUZWxlcGhvbmVcIj4xODEwMDAwMDAwMDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiUGxhY2VcIj5TdXpob3U8L2VsLWRlc2NyaXB0aW9ucy1pdGVtPlxuICAgIDxlbC1kZXNjcmlwdGlvbnMtaXRlbSBsYWJlbD1cIlJlbWFya3NcIj5cbiAgICAgIDxlbC10YWcgc2l6ZT1cInNtYWxsXCI+U2Nob29sPC9lbC10YWc+XG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJBZGRyZXNzXCI+XG4gICAgICBOby4xMTg4LCBXdXpob25nIEF2ZW51ZSwgV3V6aG9uZyBEaXN0cmljdCwgU3V6aG91LCBKaWFuZ3N1IFByb3ZpbmNlXG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgPC9lbC1kZXNjcmlwdGlvbnM+XG5cbiAgPGVsLWRlc2NyaXB0aW9uc1xuICAgIHRpdGxlPVwiV2lkdGggdmVydGljYWwgbGlzdFwiXG4gICAgZGlyZWN0aW9uPVwidmVydGljYWxcIlxuICAgIGJvcmRlclxuICAgIHN0eWxlPVwibWFyZ2luLXRvcDogMjBweFwiXG4gID5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW1cbiAgICAgIDpyb3dzcGFuPVwiMlwiXG4gICAgICA6d2lkdGg9XCIxNDBcIlxuICAgICAgbGFiZWw9XCJQaG90b1wiXG4gICAgICBhbGlnbj1cImNlbnRlclwiXG4gICAgPlxuICAgICAgPGVsLWltYWdlXG4gICAgICAgIHN0eWxlPVwid2lkdGg6IDEwMHB4OyBoZWlnaHQ6IDEwMHB4XCJcbiAgICAgICAgc3JjPVwiaHR0cHM6Ly9jdWJlLmVsZW1lY2RuLmNvbS8wLzg4LzAzYjBkMzk1ODNmNDgyMDY3NjhhNzUzNGU1NWJjcG5nLnBuZ1wiXG4gICAgICAvPlxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiVXNlcm5hbWVcIj5rb29yaW9va2FtaTwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiVGVsZXBob25lXCI+MTgxMDAwMDAwMDA8L2VsLWRlc2NyaXB0aW9ucy1pdGVtPlxuICAgIDxlbC1kZXNjcmlwdGlvbnMtaXRlbSBsYWJlbD1cIlBsYWNlXCI+U3V6aG91PC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJSZW1hcmtzXCI+XG4gICAgICA8ZWwtdGFnIHNpemU9XCJzbWFsbFwiPlNjaG9vbDwvZWwtdGFnPlxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiQWRkcmVzc1wiPlxuICAgICAgTm8uMTE4OCwgV3V6aG9uZyBBdmVudWUsIFd1emhvbmcgRGlzdHJpY3QsIFN1emhvdSwgSmlhbmdzdSBQcm92aW5jZVxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gIDwvZWwtZGVzY3JpcHRpb25zPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/descriptions/rowspan.vue)_

vue

```
<template>
  <el-descriptions title="Width horizontal list" border>
    <el-descriptions-item
      :rowspan="2"
      :width="140"
      label="Photo"
      align="center"
    >
      <el-image
        style="width: 100px; height: 100px"
        src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
      />
    </el-descriptions-item>
    <el-descriptions-item label="Username">kooriookami</el-descriptions-item>
    <el-descriptions-item label="Telephone">18100000000</el-descriptions-item>
    <el-descriptions-item label="Place">Suzhou</el-descriptions-item>
    <el-descriptions-item label="Remarks">
      <el-tag size="small">School</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="Address">
      No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
    </el-descriptions-item>
  </el-descriptions>

  <el-descriptions
    title="Width vertical list"
    direction="vertical"
    border
    style="margin-top: 20px"
  >
    <el-descriptions-item
      :rowspan="2"
      :width="140"
      label="Photo"
      align="center"
    >
      <el-image
        style="width: 100px; height: 100px"
        src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
      />
    </el-descriptions-item>
    <el-descriptions-item label="Username">kooriookami</el-descriptions-item>
    <el-descriptions-item label="Telephone">18100000000</el-descriptions-item>
    <el-descriptions-item label="Place">Suzhou</el-descriptions-item>
    <el-descriptions-item label="Remarks">
      <el-tag size="small">School</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="Address">
      No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
    </el-descriptions-item>
  </el-descriptions>
</template>
```

隐藏源代码

## 自定义样式 [​](#自定义样式)

Customized style list

<table class="el-descriptions__table is-bordered"><tbody><tr><td style="width:150px;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label is-right my-label" colspan="1">Username</td><td style="width:150px;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content is-center my-content" colspan="NaN">kooriookami</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label is-right" colspan="1">Telephone</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content is-center" colspan="NaN">18100000000</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label is-right" colspan="1">Place</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content is-center" colspan="NaN">Suzhou</td></tr><tr><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label is-right" colspan="1">Remarks</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content is-center" colspan="NaN"><span class="el-tag el-tag--primary el-tag--small el-tag--light" style="" data-v-caa66925=""><span class="el-tag__content">School</span></span></td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__label is-bordered-label is-right" colspan="1">Address</td><td style="width:;min-width:;" class="el-descriptions__cell el-descriptions__content is-bordered-content is-center" colspan="3">No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province</td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZGVzY3JpcHRpb25zIHRpdGxlPVwiQ3VzdG9taXplZCBzdHlsZSBsaXN0XCIgOmNvbHVtbj1cIjNcIiBib3JkZXI+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtXG4gICAgICBsYWJlbD1cIlVzZXJuYW1lXCJcbiAgICAgIGxhYmVsLWFsaWduPVwicmlnaHRcIlxuICAgICAgYWxpZ249XCJjZW50ZXJcIlxuICAgICAgbGFiZWwtY2xhc3MtbmFtZT1cIm15LWxhYmVsXCJcbiAgICAgIGNsYXNzLW5hbWU9XCJteS1jb250ZW50XCJcbiAgICAgIHdpZHRoPVwiMTUwcHhcIlxuICAgID5cbiAgICAgIGtvb3Jpb29rYW1pXG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJUZWxlcGhvbmVcIiBsYWJlbC1hbGlnbj1cInJpZ2h0XCIgYWxpZ249XCJjZW50ZXJcIj5cbiAgICAgIDE4MTAwMDAwMDAwXG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJQbGFjZVwiIGxhYmVsLWFsaWduPVwicmlnaHRcIiBhbGlnbj1cImNlbnRlclwiPlxuICAgICAgU3V6aG91XG4gICAgPC9lbC1kZXNjcmlwdGlvbnMtaXRlbT5cbiAgICA8ZWwtZGVzY3JpcHRpb25zLWl0ZW0gbGFiZWw9XCJSZW1hcmtzXCIgbGFiZWwtYWxpZ249XCJyaWdodFwiIGFsaWduPVwiY2VudGVyXCI+XG4gICAgICA8ZWwtdGFnIHNpemU9XCJzbWFsbFwiPlNjaG9vbDwvZWwtdGFnPlxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gICAgPGVsLWRlc2NyaXB0aW9ucy1pdGVtIGxhYmVsPVwiQWRkcmVzc1wiIGxhYmVsLWFsaWduPVwicmlnaHRcIiBhbGlnbj1cImNlbnRlclwiPlxuICAgICAgTm8uMTE4OCwgV3V6aG9uZyBBdmVudWUsIFd1emhvbmcgRGlzdHJpY3QsIFN1emhvdSwgSmlhbmdzdSBQcm92aW5jZVxuICAgIDwvZWwtZGVzY3JpcHRpb25zLWl0ZW0+XG4gIDwvZWwtZGVzY3JpcHRpb25zPlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbjpkZWVwKC5teS1sYWJlbCkge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1lbC1jb2xvci1zdWNjZXNzLWxpZ2h0LTkpICFpbXBvcnRhbnQ7XG59XG46ZGVlcCgubXktY29udGVudCkge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1lbC1jb2xvci1kYW5nZXItbGlnaHQtOSk7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/descriptions/customized-style.vue)_

vue

```
<template>
  <el-descriptions title="Customized style list" :column="3" border>
    <el-descriptions-item
      label="Username"
      label-align="right"
      align="center"
      label-class-name="my-label"
      class-name="my-content"
      width="150px"
    >
      kooriookami
    </el-descriptions-item>
    <el-descriptions-item label="Telephone" label-align="right" align="center">
      18100000000
    </el-descriptions-item>
    <el-descriptions-item label="Place" label-align="right" align="center">
      Suzhou
    </el-descriptions-item>
    <el-descriptions-item label="Remarks" label-align="right" align="center">
      <el-tag size="small">School</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="Address" label-align="right" align="center">
      No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
    </el-descriptions-item>
  </el-descriptions>
</template>

<style scoped>
:deep(.my-label) {
  background: var(--el-color-success-light-9) !important;
}
:deep(.my-content) {
  background: var(--el-color-danger-light-9);
}
</style>
```

隐藏源代码

## Descriptions API [​](#descriptions-api)

### Descriptions Attributes [​](#descriptions-attributes)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| border | 是否带有边框 | `boolean` | false |
| column | 一行 `Descriptions Item` 的数量 | `number` | 3 |
| direction | 排列的方向 | `enum` | horizontal |
| size | 列表的尺寸 | `enum` | — |
| title | 标题文本，显示在左上方 | `string` | '' |
| extra | 操作区文本，显示在右上方 | `string` | '' |
| label-width 2.8.8 | 每一列的标签宽度 | `string` / `number` | — |

### Descriptions Slots [​](#descriptions-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | Descriptions Item |
| title | 自定义标题，显示在左上方 | — |
| extra | 自定义操作区，显示在右上方 | — |

## DescriptionsItem API [​](#descriptionsitem-api)

### DescriptionsItem Attributes [​](#descriptionsitem-attributes)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| label | 标签文本 | `string` | '' |
| span | 列的数量 | `number` | 1 |
| rowspan 2.8.1 | 单元格应该跨越的行数 | `number` | 1 |
| width | 列的宽度，不同行相同列的宽度按最大值设定（如无 `border` ，宽度包含标签与内容） | `string` / `number` | '' |
| min-width | 列的最小宽度，与 `width` 的区别是 `width` 是固定的，`min-width` 会把剩余宽度按比例分配给设置了 `min-width` 的列（如无 `border`，宽度包含标签与内容） | `string` / `number` | '' |
| label-width 2.8.8 | 列标签宽，如果未设置，它将与列宽度相同。 比 `Descriptions` 的 `label-width` 优先级高 | `string` / `number` | — |
| align | 列的内容对齐方式（如无 `border`，对标签和内容均生效） | `enum` | left |
| label-align | 列的标签对齐方式，若不设置该项，则使用内容的对齐方式（如无 `border`，请使用 `align` 参数） | `enum` | — |
| class-name | 列的内容自定义类名 | `string` | '' |
| label-class-name | column label custom class name | `string` | '' |

### DescriptionsItem Slots [​](#descriptionsitem-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |
| label | 自定义标签 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/descriptions) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/descriptions.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/descriptions.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/33646534?v=4&size=64)](https://github.com/SevenDreamYang)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/34190570?v=4&size=64)](https://github.com/Lakphy)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/80440359?v=4&size=64)](https://github.com/guze2003)[![](https://avatars.githubusercontent.com/u/22659150?v=4&size=64)](https://github.com/ntnyq)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/35091020?v=4&size=64)](https://github.com/zzh948498)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/28584349?v=4&size=64)](https://github.com/wangcch)[![](https://avatars.githubusercontent.com/u/5701072?v=4&size=64)](https://github.com/Naeemo)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)

[Collapse 折叠面板](https://element-plus.org/zh-CN/component/collapse)

[Empty 空状态](https://element-plus.org/zh-CN/component/empty)


